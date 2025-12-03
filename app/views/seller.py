from flask import Blueprint,render_template,request,make_response,redirect,url_for,jsonify,flash,current_app,session
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime , timedelta
import mysql.connector
import json
import os
import base64
import io

seller_bp = Blueprint('seller',__name__,url_prefix='/seller')
# 処理方法：まず選択またはアップロードされたデータをsessionに保存され、最後にformatですべてのデータを一気にDBに登録 
#seller TOP画面表示----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller',methods=['GET'])
def seller():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
        
    resp = make_response(render_template('seller/seller_index.html', user_id = user_id))
    return resp

#seller フォーマット----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/format',methods=['GET'])
def seller_format():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
        
    # DB接続
        con = connect_db()
        cur = con.cursor(dictionary=True)
        
        #  SQL 文章用意
        sql = """
            SELECT 
                address.*             
            FROM 
                m_account AS account
            LEFT JOIN 
                m_address AS address 
            ON 
                account.id = address.account_id
            WHERE 
                account.id = %s
                ;
            """   
        cur.execute(sql, (user_id,))
        address = cur.fetchall()
        print(address)
    # address_content=""
    # for key,value in address:
    #     if address[key]:
    #         address_content += address[key]
    
    return render_template('seller/seller_format.html', 
                         user_id=user_id, 
                         )    
    # return render_template('seller/seller_format.html', user_id = user_id)

#画像アップロード画面----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/uploadImg',methods=['GET'])
def seller_uploadImg():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
      
            
    return render_template('seller/seller_uploadImg.html', user_id = user_id)

#画像アップロード----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/upload',methods=['POST'])
def seller_upload():
    file = request.files.get('file')
    if not file:
        return render_template('seller/seller_format.html')
    
    filename = secure_filename(file.filename)
    savedata = datetime.now().strftime("%Y%m%d%H%M%S_")
    filename = savedata + filename
    
    # 使用 current_app.root_path
    save_dir = os.path.join(current_app.root_path, "static", "img")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    
    #画像path生成 absolute_path
    # current_filepath = os.path.abspath(__file__)
    # current_dictionary = os.path.dirname(current_filepath)
    # save_path = current_dictionary + "\\static\\img\\" + filename
    
    #画像保存
    try:
        image = Image.open(file)
        image.save(save_path,quality = 90)
        image_url = "/static/img/" + filename      
        return jsonify({'success': True, 'image_url': image_url})
     
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
#画像アップロード----------------------------------------------------------------------------------------------------------------------------------------------------------
def seller_save_images():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'ログインが必要です'}), 401
    
    data = request.get_json()
    images = data.get('images', [])
    
    if not images:
        return jsonify({'success': False, 'error': '画像がありません'}), 400
    
    saved_urls = []
    
    try:
        for img_data in images:
            base64_str = img_data['src'].split(',')[1]
            image_bytes = base64.b64decode(base64_str)
            image = Image.open(io.BytesIO(image_bytes))
            
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{img_data['id']}.jpg"
            
            save_dir = os.path.join(current_app.root_path, "static", "img")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            
            image.save(save_path, quality=90)
            saved_urls.append(f"/static/img/{filename}")
        
        session['uploaded_images'] = saved_urls
        session.modified = True
        
        return jsonify({'success': True, 'image_urls': saved_urls})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
#size選択表示----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/size',methods=['GET'])
def seller_size():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
        
    active_tab = session.get('active_tab', 'tops')      
    selected = session.get('size_selected', {})           
    return render_template('seller/seller_size.html', user_id = user_id,selected=selected,active_tab=active_tab)

#size選択を記録----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/size/success',methods=['POST'])
def seller_size_success():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    #今のtab確認
    active_tab = request.form.get('active_tab', 'tops')
    session['active_tab'] = active_tab
    
    size_field = ['shoulderWidth', 'bodyWidth', 'sleeveLength', 'bodyLength','notes','hip','totalLength','rise','inseam','waist','thighWidth','hemWidth','skirtLength']
    tops_fields = ['shoulderWidth', 'bodyWidth', 'sleeveLength', 'bodyLength', 'notes']
    bottoms_fields = ['hip', 'totalLength', 'rise', 'inseam', 'waist', 'thighWidth', 'hemWidth', 'skirtLength', 'notes']
    
    size_data = {s: request.form.get(s, '') for s in size_field}
    
    if active_tab == 'tops':
        filtered_data = {k: v for k, v in size_data.items() if k in tops_fields}
    else:
        filtered_data = {k: v for k, v in size_data.items() if k in bottoms_fields}
        
    session['size_selected'] = filtered_data
 
    print(f" Active tab: {active_tab}")
    print(f" Saved data: {filtered_data}")
    
    return redirect(url_for('seller.seller_format'))
    
#サイズ記録----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/get_size_selected')
def get_size_selected():
    return jsonify(session.get('size_selected', {}))
#洗濯表示----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/clean',methods=['GET'])
def seller_clean():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
      
    selected = session.get('clean_selected', {})
    print(selected)
    return render_template('seller/seller_clean.html', selected=selected, user_id=user_id)           

#洗濯表示記録----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/clean/success',methods=['POST'])
def seller_clean_success():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    #取ってきたデータを辞書型で保存
    session['clean_selected'] = request.form.to_dict()
    return redirect(url_for('seller.seller_format'))          
    # return render_template('seller/seller_format.html', user_id = user_id)

#洗濯表示記録----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/get_clean_selected')
def get_clean_selected():
    return jsonify(session.get('clean_selected', {}))

#セラーフォマットの内容をDB登録----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/format/save-product', methods=['POST'])
def save_product():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    try:
        product_data_str = request.form.get('productData')
        if not product_data_str:
            return jsonify({
                'success': False,
                'message': '商品情報がありません'
            }), 400

        data = json.loads(product_data_str)
        print(data)
        con = connect_db()
        cursor = con.cursor()
        
                    
        #  SQL 文章用意
        sql = """
            INSERT INTO m_product (
                name, 
                purchasePrice, 
                rentalPrice,
                size,
                color, 
                `for`, 
                upload, 
                showing, 
                draft, 
                updateDate, 
                purchaseFlg, 
                rentalFlg, 
                explanation, 
                account_id,
                brand_id, 
                category_id, 
                cleanNotes, 
                smokingFlg, 
                returnAddress,
                `condition`,
                rentalPeriod
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s
            )
        """
        
        # 時間
        current_date = datetime.now().date()
        current_datetime = datetime.now()
        
        #実際の資料
        values = (
            data.get('name'),          
            int(data.get('purchasePrice')) if data.get('purchasePrice') else None,
            int(data.get('rentalPrice')) if data.get('rentalPrice') else None,
            session.get('size_selected', {}).get('notes'),
            data.get('color'),
            data.get('category1', 'ユニセックス'), 
            current_date,
            '公開', 
            0,
            current_datetime,
            1 if data.get('purchase') else 0,
            1 if data.get('rental') else 0,
            data.get('explanation') if data.get('explanation') else None,
            session.get('user_id'),      
            int(data.get('brand')) if data.get('brand') else None,
            int(data.get('category2')) if data.get('category2') else None, 
            session.get('clean_selected', {}).get('notes'),  # 注意事項
            1 if data.get('smoking') else 0,
            data.get('returnLocation') if data.get('returnLocation') else None,
            '取引可',
            int(data.get('rentalPeriod')) if data.get('rentalPeriod') else None
        )
        #  SQL 実行
        cursor.execute(sql, values)
        con.commit()

        # AUTO INCREMENTの値を取得
        product_id = cursor.lastrowid
        
        #====== size登録の処理 ==============================================================================================================
        #今のtab確認
        active_tab = session.get('active_tab')
        size_selected = session.get('size_selected', {})           
        # tops bottomsの判断######################################################
        if active_tab == 'tops':
            sql = """
                INSERT INTO m_topssize (
                    product_id, shoulderWidth, bodyWidth, sleeveLength, bodyLength, notes
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )
            """
            values = (
                product_id,
                size_selected.get('shoulderWidth'),
                size_selected.get('bodyWidth'),
                size_selected.get('sleeveLength'),
                size_selected.get('bodyLength'),
                size_selected.get('notes'),
            )                    
        else:          
            sql = """
                INSERT INTO m_bottomssize (
                    product_id, hip, totalLength, rise, inseam, waist, thighWidth, hemWidth, skirtLength, notes
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            values = (
                product_id,
                size_selected.get('hip'),
                size_selected.get('totalLength'),
                size_selected.get('rise'),
                size_selected.get('inseam'),
                size_selected.get('waist'),
                size_selected.get('thighWidth'),
                size_selected.get('hemWidth'),
                size_selected.get('skirtLength'),
                size_selected.get('notes'),
            )
            
        cursor.execute(sql, values)
        con.commit()
        #====== clean登録の処理 ============================================================================================================== 
        clean_selected = session.get('clean_selected', {})
            
        # clean フィールド名を定義
        clean_fields = ['wash', 'bleach', 'tumble', 'dry', 'iron', 'dryclean', 'wet']
        
        inserted_count = 0
        try:
            # すべての項目確認
            for field_name in clean_fields:
                val = clean_selected.get(field_name)  # フィールド値を取得
                
                # "None"、''の場合は処理しない
                if val in [None, '', 'None']:
                    continue
                
                # SQL用意
                sql = """
                    INSERT INTO t_clean (product_id, cleanSign_id)
                    VALUES (%s, %s)
                """
                values = (product_id, val)
        
                cursor.execute(sql, values)
                inserted_count += 1

            con.commit()

        except Exception as e:
            # エラーが発生するとき、前の処理なかったことにする
            print(f' t_clean 登録エラー: {str(e)}')  #  デバッグ用
            con.rollback()
            
            
        # ===== 画像アップロードの処理 =====
        uploaded_image_count = 0
        
        if 'images' in request.files:
            files = request.files.getlist('images')
            print(f'画像の数: {len(files)}')

            # uploadsフォルダー指定、なければつくる
            upload_folder = 'app/static/img/productImg'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            for index, file in enumerate(files):
                try:
                    if file and file.filename:
                        # ===== 唯一の画像名を生成 =====
                        timestamp = int(datetime.now().timestamp() * 1000)
                        filename = f"product_{product_id}_{index}_{timestamp}.png"
                        filepath = os.path.join(upload_folder, filename)

                        # ===== ファイル保存 =====
                        file.save(filepath)
                        print(f'画像{index}保存済み: {filename}')

                        # ===== m_productimg =====
                        # user_id, product_id, imgカラムと合わせる
                        cursor.execute(
                            "INSERT INTO m_productimg (product_id, img) VALUES (%s, %s)",
                            (int(product_id), filename)
                        )
                        con.commit()
                        uploaded_image_count += 1
                        print(f'画像DB登録完了: user_id={user_id}, product_id={product_id}, img={filename}')

                except Exception as img_error:
                    print(f'画像{index}アップロード失敗: {str(img_error)}')
                    con.rollback()
                    continue

        else:
            print('画像がない')
        
        
        cursor.close()
        con.close()
        
        #session削除
        session.pop('size_selected', None)
        session.pop('clean_selected', None)
        
        return jsonify({
            'success': True,
            'message': 'DBの登録成功',
            'product_id': product_id
        }), 200
        
    except mysql.connector.Error as err:
        return jsonify({
            'success': False,
            'message': f'DBエラー: {str(err)}'
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'わからないエラー: {str(e)}'
        }), 500


#セラーフォマットの内容を下書きのDB登録----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/format/save-product-draft', methods=['POST'])
def save_product_draft():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
        
    try:
        product_data_str = request.form.get('productData')
        if not product_data_str:
            return jsonify({
                'success': False,
                'message': '商品情報がありません'
            }), 400

        # 解析JSON
        data = json.loads(product_data_str)
        # data = request.get_json()
        
        # DB接続
        con = connect_db()
        cursor = con.cursor()
        
        #  SQL 文章用意
        sql = """
            INSERT INTO m_product (
                name, 
                purchasePrice, 
                rentalPrice,
                size,
                color, 
                `for`, 
                upload, 
                showing, 
                draft, 
                updateDate, 
                purchaseFlg, 
                rentalFlg, 
                explanation, 
                account_id,
                brand_id, 
                category_id, 
                cleanNotes, 
                smokingFlg, 
                returnAddress,
                `condition`,
                rentalPeriod
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s
            )
        """
        
        # 時間
        current_date = datetime.now().date()
        current_datetime = datetime.now()
        
        #実際の資料
        values = (
            data.get('name'),          
            int(data.get('purchasePrice')) if data.get('purchasePrice') else None,
            int(data.get('rentalPrice')) if data.get('rentalPrice') else None,
            session.get('size_selected', {}).get('notes'),
            data.get('color'),
            data.get('category1', 'ユニセックス'), 
            current_date,
            '公開', 
            1,
            current_datetime,
            1 if data.get('purchase') else 0,
            1 if data.get('rental') else 0,
            data.get('explanation') if data.get('explanation') else None,
            session.get('user_id'),      
            int(data.get('brand')) if data.get('brand') else None,
            int(data.get('category2')) if data.get('category2') else None, 
            session.get('clean_selected', {}).get('notes'),  # 注意事項
            1 if data.get('smoking') else 0,
            data.get('returnLocation') if data.get('returnLocation') else None,
            '取引可',
            int(data.get('rentalPeriod')) if data.get('rentalPeriod') else None
        )
        
        # 除錯：打印 SQL 和值
        print("SQL:", sql)
        print("Values count:", len(values))
        print("Values:", values)    
        #  SQL 実行
        cursor.execute(sql, values)
        con.commit()
        
        # AUTO INCREMENTの値を取得
        product_id = cursor.lastrowid
        
        #====== size登録の処理 ==============================================================================================================
        #今のtab確認
        active_tab = session.get('active_tab')
        size_selected = session.get('size_selected', {})
        
        # tops bottomsの判断######################################################
        if active_tab == 'tops':
            sql = """
                INSERT INTO m_topssize (
                    product_id, shoulderWidth, bodyWidth, sleeveLength, bodyLength, notes
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )
            """
            values = (
                product_id,
                size_selected.get('shoulderWidth'),
                size_selected.get('bodyWidth'),
                size_selected.get('sleeveLength'),
                size_selected.get('bodyLength'),
                size_selected.get('notes'),
            )
            
        if active_tab =="bottoms":
            sql = """
                INSERT INTO m_bottomssize (
                    product_id, hip, totalLength, rise, inseam, waist, thighWidth, hemWidth, skirtLength, notes
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            values = (
                product_id,
                size_selected.get('hip'),
                size_selected.get('totalLength'),
                size_selected.get('rise'),
                size_selected.get('inseam'),
                size_selected.get('waist'),
                size_selected.get('thighWidth'),
                size_selected.get('hemWidth'),
                size_selected.get('skirtLength'),
                size_selected.get('notes'),
            )
        print(active_tab)    
        cursor.execute(sql, values)
        con.commit()
        #====== clean登録の処理 ============================================================================================================== 
        clean_selected = session.get('clean_selected', {})
        
        # clean フィールド名を定義
        clean_fields = ['wash', 'bleach', 'tumble', 'dry', 'iron', 'dryclean', 'wet']
        
        inserted_count = 0
        try:
            # すべての項目確認
            for field_name in clean_fields:
                val = clean_selected.get(field_name)  # フィールド値を取得
                
                # "None"、''の場合は処理しない
                if val in [None, '', 'None']:
                    continue
                
                # SQL用意
                sql = """
                    INSERT INTO t_clean (product_id, cleanSign_id)
                    VALUES (%s, %s)
                """
                values = (product_id, val)
        
                cursor.execute(sql, values)
                inserted_count += 1

            con.commit()

        except Exception as e:
            # エラーが発生するとき、前の処理なかったことにする
            print(f' t_clean 登録エラー: {str(e)}')  #  デバッグ用
            con.rollback()
            
            
        # ===== 画像アップロードの処理 =====
        uploaded_image_count = 0
        
        if 'images' in request.files:
            files = request.files.getlist('images')
            print(f'画像の数: {len(files)}')

            # uploadsフォルダー指定、なければつくる
            upload_folder = 'app/static/img/productImg'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            for index, file in enumerate(files):
                try:
                    if file and file.filename:
                        # ===== 唯一の画像名を生成 =====
                        timestamp = int(datetime.now().timestamp() * 1000)
                        filename = f"product_{product_id}_{index}_{timestamp}.png"
                        filepath = os.path.join(upload_folder, filename)

                        # ===== ファイル保存 =====
                        file.save(filepath)
                        print(f'画像{index}保存済み: {filename}')

                        # ===== m_productimg =====
                        # user_id, product_id, imgカラムと合わせる
                        cursor.execute(
                            "INSERT INTO m_productimg (product_id, img) VALUES (%s, %s)",
                            (int(product_id), filename)
                        )
                        con.commit()
                        uploaded_image_count += 1
                        print(f'画像DB登録完了: user_id={user_id}, product_id={product_id}, img={filename}')

                except Exception as img_error:
                    print(f'画像{index}アップロード失敗: {str(img_error)}')
                    con.rollback()
                    continue

        else:
            print('画像がない')
        
        cursor.close()
        con.close()
        
        #session削除
        session.pop('size_selected', None)
        session.pop('clean_selected', None)
        
        return jsonify({
            'success': True,
            'message': '下書きDBの登録成功',
            'product_id': product_id
        }), 200
        
    except mysql.connector.Error as err:
        return jsonify({
            'success': False,
            'message': f'DBエラー: {str(err)}'
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'わからないエラー: {str(e)}'
        }), 500

#出品一覧画面----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/products',methods=['GET'])
def seller_products():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
        
        # DB接続
        con = connect_db()
        cur = con.cursor(dictionary=True)
        
        #  SQL 文章用意すべての商品
        sql = """
            SELECT 
                p.*, 
                m.img
            FROM 
                m_product AS p
            LEFT JOIN 
                m_productimg AS m 
            ON 
                p.id = m.product_id
            WHERE 
                p.account_id = %s
            AND
                p.draft = 0
            ;
            """   
        cur.execute(sql, (user_id,))
        products = cur.fetchall()
        print(products)
        #  SQL 文章用意　最近商品
        sql = """
            SELECT 
                p.*, 
                m.img
            FROM 
                m_product AS p
            LEFT JOIN 
                m_productimg AS m 
            ON 
                p.id = m.product_id
            WHERE 
                p.account_id = %s
            AND
                p.draft = 0
            ORDER BY p.id DESC
            LIMIT 1
            ;
            """   
        cur.execute(sql, (user_id,))
        recent = cur.fetchone()
        
        cur.close()
        con.close()
        #出品商品の表示 products={product_id:2, customer_id:1, status:2, ...}
        

    return render_template('seller/seller_products.html',products=products, recent=recent, user_id = user_id)

#下書き一覧画面----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/seller/draft',methods=['GET'])
def seller_draft():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    # DB接続
        con = connect_db()
        cur = con.cursor(dictionary=True)
        
        #  SQL 文章用意
        sql = """
            SELECT 
                p.*, 
                m.img
            FROM 
                m_product AS p
            LEFT JOIN 
                m_productimg AS m 
            ON 
                p.id = m.product_id
            WHERE 
                p.account_id = %s
            AND
                p.draft = 1
                ;
            """   
        cur.execute(sql, (user_id,))
        products = cur.fetchall()
       
        #  SQL 文章用意
        sql = """
            SELECT 
                p.*, 
                m.img
            FROM 
                m_product AS p
            LEFT JOIN 
                m_productimg AS m 
            ON 
                p.id = m.product_id
            WHERE 
                p.account_id = %s
            AND
                p.draft = 1
            ORDER BY p.id DESC
            LIMIT 1
            ;
            """   
        cur.execute(sql, (user_id,))
        recent = cur.fetchone()
        cur.close()
        con.close()
        #出品商品の表示 products={product_id:2, customer_id:1, status:2, ...}
      
            
    return render_template('seller/seller_draft.html', products=products, recent=recent, user_id = user_id)  
 
#データセンター覧画面----------------------------------------------------------------------------------------------------------------------------------------------------------
# @seller_bp.route('/datacenter',methods=['GET'])
# def datacenter():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
      
            
    return render_template('seller/seller_datacenter.html', user_id = user_id)

#商品アップデート画面----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/update/<int:product_id>',methods=['GET'])
def update(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    user_id = session.get('user_id')
    
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        
        # データ取得
        sql = """
            SELECT *
            FROM m_product
            WHERE id = %s AND account_id = %s
        """
        cur.execute(sql, (product_id, user_id))
        product = cur.fetchone()
        print("product:",product)
        if not product:
            cur.close()
            con.close()
            return redirect(url_for('seller.seller_products'))
        
        # サイズ取得
        category2 = product.get('category_id')
        size_data = {}
        if category2 == 2 :  # トップス
            sql = "SELECT * FROM m_topssize WHERE product_id = %s"
            cur.execute(sql, (product_id,))
            size_data = cur.fetchone() or {}
            session['active_tab'] = 'tops'
        else:  # ボトムス
            sql = "SELECT * FROM m_bottomssize WHERE product_id = %s"
            cur.execute(sql, (product_id,))
            size_data = cur.fetchone() or {}
            session['active_tab'] = 'bottoms'
        size_data['notes'] = product['size']
        print("size_data:",size_data)
        # 洗濯表示
        sql = "SELECT cleanSign_id FROM t_clean WHERE product_id = %s"
        cur.execute(sql, (product_id,))
        clean_results = cur.fetchall()
        clean_data = {}
        print("clean_results",clean_results)
        if clean_results:
            clean_sign_to_field = {
                'wash': ['190','170','160','161','150','151','140','141','142','130','131','132','110','111','100'],
                'bleach': ['220','210','200'],
                'tumble': ['320','310','300'],
                'dry': ['440','445','430','435','420','425','410','415'],
                'iron': ['530','520','510','511','500'],
                'dryclean': ['620','621','610','611','600'],
                'wet': ['710','711','712','700']
                }    
            for row in clean_results:
                sign_id = str(row['cleanSign_id'])
                #  cleanSign_id の field name
                for field_name, values in clean_sign_to_field.items():
                    if sign_id in values:
                        clean_data[field_name] = sign_id
                        break
            
        clean_data['note'] = product['cleanNotes'] 
        cur.close()
        con.close()
        # print("===================================")
        # print(clean_data)
        #  session
        session['size_selected'] = size_data
        session['clean_selected'] = clean_data
        session['edit_product_id'] = product_id
        session.modified = True
        # print(session['clean_selected'])
        return render_template('seller/seller_update.html',
                             user_id=user_id,
                             product=product)
    
    except Exception as e:
        print(f'エラー: {str(e)}')
        return redirect(url_for('seller.seller_products'))

#商品更新の内容をDB登録----------------------------------------------------------------------------------------------------------------------------------------------------------
@seller_bp.route('/format/update-product', methods=['POST'])
def update_product():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    #編集モード確認
    edit_product_id = session.get('edit_product_id')
    
    try:
        product_data_str = request.form.get('productData')
        if not product_data_str:
            return jsonify({
                'success': False,
                'message': '商品情報がありません'
            }), 400

        data = json.loads(product_data_str)
        print(data)
        con = connect_db()
        cursor = con.cursor()
        
        if edit_product_id:
            # 編輯模式：UPDATE
            sql = """
                UPDATE m_product
                SET name = %s,
                    purchasePrice = %s,
                    rentalPrice = %s,
                    rentalPeriod = %s,
                    color = %s,
                    explanation = %s,
                    purchaseFlg = %s,
                    rentalFlg = %s,
                    smokingFlg = %s,
                    returnAddress = %s,
                    updateDate = %s
                WHERE id = %s AND account_id = %s
            """
            
            values = (
                data.get('name'),
                int(data.get('purchasePrice')) if data.get('purchasePrice') else None,
                int(data.get('rentalPrice')) if data.get('rentalPrice') else None,
                int(data.get('rentalPeriod')) if data.get('rentalPeriod') else None,
                data.get('color'),
                data.get('explanation') if data.get('explanation') else None,
                1 if data.get('purchase') else 0,
                1 if data.get('rental') else 0,
                1 if data.get('smoking') else 0,
                data.get('returnLocation') if data.get('returnLocation') else None,
                datetime.now(),
                edit_product_id,
                user_id
            )
            
            cursor.execute(sql, values)
            con.commit()
            product_id = edit_product_id
            
        else:            
            #  SQL 文章用意
            sql = """
                INSERT INTO m_product (
                    name, 
                    purchasePrice, 
                    rentalPrice,
                    rentalPeriod, 
                    size,
                    color, 
                    `for`, 
                    upload, 
                    showing, 
                    draft, 
                    updateDate, 
                    purchaseFlg, 
                    rentalFlg, 
                    explanation, 
                    account_id,
                    brand_id, 
                    category_id, 
                    cleanNotes, 
                    smokingFlg, 
                    returnAddress
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s
                )
            """
            
            # 時間
            current_date = datetime.now().date()
            current_datetime = datetime.now()
            
            #実際の資料
            values = (
                data.get('name'),          
                int(data.get('purchasePrice')) if data.get('purchasePrice') else None,
                int(data.get('rentalPrice')) if data.get('rentalPrice') else None,
                int(data.get('rentalPeriod')) if data.get('rentalPeriod') else None,
                session.get('size_selected', {}).get('notes'),
                data.get('color'),
                data.get('category1', 'ユニセックス'), 
                current_date,
                '公開', 
                0,
                current_datetime,
                1 if data.get('purchase') else 0,
                1 if data.get('rental') else 0,
                data.get('explanation') if data.get('explanation') else None,
                session.get('user_id'),      
                int(data.get('brand')) if data.get('brand') else None,
                int(data.get('category2')) if data.get('category2') else None, 
                session.get('clean_selected', {}).get('notes'),  # 注意事項
                1 if data.get('smoking') else 0,
                data.get('returnLocation') if data.get('returnLocation') else None
            )
            
            #  SQL 実行
            cursor.execute(sql, values)
            con.commit()
            
            # AUTO INCREMENTの値を取得
            product_id = cursor.lastrowid
            
            #====== size登録の処理 ==============================================================================================================
            #今のtab確認
            active_tab = session.get('active_tab')
            size_selected = session.get('size_selected', {})           
            # tops bottomsの判断######################################################
            if active_tab == 'tops':
                if edit_product_id:
                    sql = """
                        UPDATE m_topssize
                        SET shoulderWidth = %s, bodyWidth = %s, sleeveLength = %s,
                            bodyLength = %s, notes = %s
                        WHERE product_id = %s
                    """
                    values = (
                        size_selected.get('shoulderWidth'),
                        size_selected.get('bodyWidth'),
                        size_selected.get('sleeveLength'),
                        size_selected.get('bodyLength'),
                        size_selected.get('notes'),
                        product_id
                    )
                else:
                    sql = """
                        INSERT INTO m_topssize (
                            product_id, shoulderWidth, bodyWidth, sleeveLength, bodyLength, notes
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s
                        )
                    """
                    values = (
                        product_id,
                        size_selected.get('shoulderWidth'),
                        size_selected.get('bodyWidth'),
                        size_selected.get('sleeveLength'),
                        size_selected.get('bodyLength'),
                        size_selected.get('notes'),
                    )
                    
            else:
                if edit_product_id:
                    sql = """
                        UPDATE m_bottomssize
                        SET hip = %s, totalLength = %s, rise = %s, inseam = %s,
                            waist = %s, thighWidth = %s, hemWidth = %s, skirtLength = %s, notes = %s
                        WHERE product_id = %s
                    """
                    values = (
                        size_selected.get('hip'),
                        size_selected.get('totalLength'),
                        size_selected.get('rise'),
                        size_selected.get('inseam'),
                        size_selected.get('waist'),
                        size_selected.get('thighWidth'),
                        size_selected.get('hemWidth'),
                        size_selected.get('skirtLength'),
                        size_selected.get('notes'),
                        product_id
                    )
                else:
                    sql = """
                        INSERT INTO m_bottomssize (
                            product_id, hip, totalLength, rise, inseam, waist, thighWidth, hemWidth, skirtLength, notes
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    values = (
                        product_id,
                        size_selected.get('hip'),
                        size_selected.get('totalLength'),
                        size_selected.get('rise'),
                        size_selected.get('inseam'),
                        size_selected.get('waist'),
                        size_selected.get('thighWidth'),
                        size_selected.get('hemWidth'),
                        size_selected.get('skirtLength'),
                        size_selected.get('notes'),
                    )
                
            cursor.execute(sql, values)
            con.commit()
            #====== clean登録の処理 ============================================================================================================== 
            clean_selected = session.get('clean_selected', {})
            
            if edit_product_id:
                cursor.execute("DELETE FROM t_clean WHERE product_id = %s", (product_id,))
                con.commit()
            # clean フィールド名を定義
            clean_fields = ['wash', 'bleach', 'tumble', 'dry', 'iron', 'dryclean', 'wet']
            
            inserted_count = 0
            try:
                # すべての項目確認
                for field_name in clean_fields:
                    val = clean_selected.get(field_name)  # フィールド値を取得
                    
                    # "None"、''の場合は処理しない
                    if val in [None, '', 'None']:
                        continue
                    
                    # SQL用意
                    sql = """
                        INSERT INTO t_clean (product_id, cleanSign_id)
                        VALUES (%s, %s)
                    """
                    values = (product_id, val)
            
                    cursor.execute(sql, values)
                    inserted_count += 1

                con.commit()

            except Exception as e:
                # エラーが発生するとき、前の処理なかったことにする
                print(f' t_clean 登録エラー: {str(e)}')  #  デバッグ用
                con.rollback()
                
            
        # ===== 画像アップロードの処理 =====
        uploaded_image_count = 0
        
        if 'images' in request.files:
            files = request.files.getlist('images')
            print(f'画像の数: {len(files)}')

            # uploadsフォルダー指定、なければつくる
            upload_folder = 'app/static/img/productImg'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            for index, file in enumerate(files):
                try:
                    if file and file.filename:
                        # ===== 唯一の画像名を生成 =====
                        timestamp = int(datetime.now().timestamp() * 1000)
                        filename = f"product_{product_id}_{index}_{timestamp}.png"
                        filepath = os.path.join(upload_folder, filename)

                        # ===== ファイル保存 =====
                        file.save(filepath)
                        print(f'画像{index}保存済み: {filename}')

                        # ===== m_productimg =====
                        # user_id, product_id, imgカラムと合わせる
                        cursor.execute(
                            "INSERT INTO m_productimg (product_id, img) VALUES (%s, %s)",
                            (int(product_id), filename)
                        )
                        con.commit()
                        uploaded_image_count += 1
                        print(f'画像DB登録完了: user_id={user_id}, product_id={product_id}, img={filename}')

                except Exception as img_error:
                    print(f'画像{index}アップロード失敗: {str(img_error)}')
                    con.rollback()
                    continue

        else:
            print('画像がない')
        
        cursor.close()
        con.close()
        
        #session削除
        session.pop('size_selected', None)
        session.pop('clean_selected', None)
        session.pop('edit_product_id', None)
        
        return jsonify({
            'success': True,
            'message': 'DBの登録成功',
            'product_id': product_id
        }), 200
        
    except mysql.connector.Error as err:
        return jsonify({
            'success': False,
            'message': f'DBエラー: {str(err)}'
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'わからないエラー: {str(e)}'
        }), 500

#削除------------------------------------------------------------------------------------------------------------------------------------------------------#
@seller_bp.route('/format/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'ログインが必要です'}), 401
    
    user_id = session.get('user_id')
    
    try:
        con = connect_db()
        cursor = con.cursor(dictionary=True)
        #取引中確認
        sql = """
                SELECT t.status FROM m_product AS p
                LEFT JOIN t_transaction AS t
                ON p.id = t.product_id
                WHERE p.id = %s
                LIMIT 1
                ;                
        """
        cursor.execute(sql,(product_id,))
        status = cursor.fetchone()
        if status['status'] =="取引完了" or status['status'] is None: 
            # 画像
            cursor.execute("DELETE FROM m_productimg WHERE product_id = %s", (product_id,))
            
            # サイズ
            cursor.execute("DELETE FROM m_topssize WHERE product_id = %s", (product_id,))
            cursor.execute("DELETE FROM m_bottomssize WHERE product_id = %s", (product_id,))
            
            # 洗濯
            cursor.execute("DELETE FROM t_clean WHERE product_id = %s", (product_id,))
            
            #コメント
            cursor.execute("DELETE FROM t_comments WHERE product_id = %s", (product_id,))
            
            # ほか
            cursor.execute("DELETE FROM m_product WHERE id = %s", (product_id,))
            
            con.commit()
            cursor.close()
            con.close()
            
        else:
            cursor.close()
            con.close()
            return jsonify({'success':False,'message':'取引中は削除できません'})
        return jsonify({'success': True, 'message': '商品を削除しました'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'エラー: {str(e)}'}), 500
    

#DB設定------------------------------------------------------------------------------------------------------------------------------------------------------------------
def connect_db():
    con=mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = '',
        db ='db_subkari',
        
    )
    return con