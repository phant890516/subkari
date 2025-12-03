from flask import Blueprint, render_template, request, make_response, redirect, url_for, current_app, session,jsonify
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import mysql.connector
import json
import os

deal_bp = Blueprint('deal', __name__, url_prefix='/deal')


# 取引TOP画面表示 ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/deal', methods=['GET'])
def deal():
    # user検証成功
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
     
        # DB接続
        con = connect_db()
        cur = con.cursor(dictionary=True)
        
        #  SQL 文章用意bought
        sql = """
            SELECT 
                p.*, 
                m.img,
                t.id,
                t.status,
                t.situation,
                t.date
            FROM 
                m_product AS p
            LEFT JOIN 
                m_productimg AS m 
            ON 
                p.id = m.product_id
            LEFT JOIN 
                t_transaction AS t 
            ON 
                p.id = t.product_id
            WHERE 
                t.customer_id = %s
            ORDER BY p.id ASC
            ;
            """   
        cur.execute(sql, (user_id,))
        bought_products = cur.fetchall()
       
        #  SQL 文章用意sell
        sql = """
            SELECT 
                p.*, 
                m.img,
                t.id,
                t.status,t.situation,t.date
            FROM 
                m_product AS p
            LEFT JOIN 
                m_productimg AS m 
            ON 
                p.id = m.product_id
            LEFT JOIN 
                t_transaction AS t 
            ON 
                p.id = t.product_id
            WHERE 
                p.account_id = %s
            AND
                p.draft = 0
            AND
                t.status IS NOT NULL
            GROUP BY p.id
            ;
            """   
        cur.execute(sql, (user_id,))
        products = cur.fetchall()
        cur.close()
        con.close()
        #出品商品の表示 products={product_id:2, customer_id:1, status:2, ...}
        
        
    return render_template('deal/deal_index.html', bought_products = bought_products, products = products, user_id = user_id)
# 取引商品詳細の表示（購入側） ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/deal/<int:transaction_id>', methods=['GET','POST'])
def deal_list(transaction_id):
    # euser検証成功
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    #取引資料の取得-------------------------------------------------------------
    # DB接続
    con = connect_db()
    cur = con.cursor(dictionary=True)  
    #  SQL 文章用意
    sql = """
        SELECT 
            t.*,
            p.rentalPrice,
            p.purchasePrice,
            m.img
        FROM 
            t_transaction AS t
        LEFT JOIN 
            m_product AS p
        ON
            t.product_id = p.id
        LEFT JOIN 
            m_productimg AS m
        ON
            t.product_id = m.product_id
        WHERE 
            t.id = %s
        LIMIT 1
        ;
        """
    cur.execute(sql, (transaction_id,))
    transaction = cur.fetchone()
    
    if not transaction:
        return redirect(url_for('deal.deal'))
    
    if transaction.get('shippingPhoto'):
        transaction['shippingPhoto'] = f"/static/img/{transaction['shippingPhoto']}"
    if transaction.get('cleaningPhoto'):
        transaction['cleaningPhoto'] = f"/static/img/{transaction['cleaningPhoto']}"
    if transaction.get('receivedPhoto'):
        transaction['receivedPhoto'] = f"/static/img/{transaction['receivedPhoto']}"
          
    session['transaction'] = transaction
    
    # commentsの取得
    product_id = transaction['product_id']
    sql = """
        SELECT content, createdDate, account_id
        FROM t_comments
        WHERE product_id = %s
        ORDER BY createdDate DESC
    """
    cur.execute(sql, (product_id,))
    comments = cur.fetchall()
    cur.close()
    con.close()   
    
    if transaction['situation'] == '購入':
        charge = int(transaction.get('purchasePrice') or 0) * 0.1
        benefit = int(transaction['purchasePrice']) - charge
        transaction['charge'] = charge
        transaction['benefit'] = benefit
        
    if transaction['situation'] == 'レンタル':
        charge = int(transaction['rentalPrice'])*0.1
        benefit = int(transaction['rentalPrice']) - charge
        transaction['charge'] = charge
        transaction['benefit'] = benefit
        
    print(transaction)
    
    return render_template('deal/deal_detail.html', transaction = transaction,comments = comments, user_id = user_id)

# 取引商品詳細の表示（出品側） ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/deal_seller/<int:transaction_id>', methods=['GET','POST'])
def deal_list_seller(transaction_id):
       # euser検証成功
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    #取引資料の取得-------------------------------------------------------------
    # DB接続
    con = connect_db()
    cur = con.cursor(dictionary=True)  
    #  SQL 文章用意
    sql = """
        SELECT 
            t.*,
            p.rentalPrice,
            p.purchasePrice,
            m.img
        FROM 
            t_transaction AS t
        LEFT JOIN 
            m_product AS p
        ON
            t.product_id = p.id
        LEFT JOIN 
            m_productimg AS m
        ON
            t.product_id = m.product_id
        WHERE 
            t.id = %s
        LIMIT 1
        ;
        """
    cur.execute(sql, (transaction_id,))
    transaction = cur.fetchone()
    
    if not transaction:
        return redirect(url_for('deal.deal')) 
    
    if transaction.get('shippingPhoto'):
        transaction['shippingPhoto'] = f"/static/img/{transaction['shippingPhoto']}"
    if transaction.get('cleaningPhoto'):
        transaction['cleaningPhoto'] = f"/static/img/{transaction['cleaningPhoto']}"
    if transaction.get('receivedPhoto'):
        transaction['receivedPhoto'] = f"/static/img/{transaction['receivedPhoto']}"    
    
    session['transaction'] = transaction    
    # commentsの取得
    product_id = transaction['product_id']
    sql = """
        SELECT content, createdDate, account_id
        FROM t_comments
        WHERE product_id = %s
        ORDER BY createdDate DESC
    """
    cur.execute(sql, (product_id,))
    comments = cur.fetchall()
    cur.close()
    con.close()   
    
    if transaction['situation'] == '購入':
        charge = int(transaction.get('purchasePrice') or 0) * 0.1
        benefit = int(transaction['purchasePrice']) - charge
        transaction['charge'] = charge
        transaction['benefit'] = benefit
        
    if transaction['situation'] == 'レンタル':
        charge = int(transaction['rentalPrice'])*0.1
        benefit = int(transaction['rentalPrice']) - charge
        transaction['charge'] = charge
        transaction['benefit'] = benefit
        
    print(transaction)
    
    return render_template('deal/deal_seller_detail.html', transaction = transaction,comments = comments, user_id = user_id)

# 出品者資料の取得--------------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/seller_data/get/<int:customer_id>',methods=['GET'])
def get_seller_data(customer_id):
    
    try:
        seller_data = get_seller_info(customer_id)
        print(seller_data)
        return jsonify({'success':True,
                    'data':seller_data})

    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'success': False, 'message': str(e)}), 500

#商品の出品者資料--------------------------------------------------
def get_seller_info(id):
    con = connect_db()
    cur = con.cursor(dictionary=True)

    #firstName identifyImg status smoker evaluation total
    sql = """
            SELECT 
                a.firstName,
                a.profileImage,
                a.status,
                a.smoker,
                COUNT(e.id) as evaluation_count,
                ROUND(AVG(e.score),1) as average_score
            FROM m_account a
            LEFT JOIN t_evaluation e
            ON a.id = e.recipient_id
            WHERE a.id=%s
            GROUP BY a.id           
        """
    cur.execute(sql,(id,))
    result = cur.fetchone()
    cur.close()
    con.close()
    
    return result    
     
# cleaning取引詳細の画像添付 ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/deal/list/imageUpload/<int:transaction_id>', methods=['GET','POST'])
def deal_list_imageUpload(transaction_id):
    # euser検証成功
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    #アップロードと送信の判断
    if request.method == 'GET':
        return render_template('deal/deal_detail.html', 
                             upload_success=False, 
                             user_id=user_id)
        
    if 'img' not in request.files or not request.files['img'].filename:
        error = "ファイルが選択されていません"
        return render_template('deal/deal_detail.html', 
                             upload_success=False, 
                             error=error, 
                             user_id=user_id)
    
    transaction = session.get('transaction')
    #ここから    
    file = request.files['img']
    
    # 画像検証
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        error = "許可されていないファイル形式です"
        return render_template('deal/deal_detail.html', 
                             upload_success=False, 
                             error=error, 
                             user_id=user_id,
                             transaction = transaction)
    
    try:
        # システム用的画像名を生成
        filename = secure_filename(file.filename)
        savedata = datetime.now().strftime("%Y%m%d%H%M%S_")
        filename = savedata + filename
        
        # 保存パス生成
        # current_filepath = os.path.abspath(__file__)
        # current_dictionary = os.path.dirname(current_filepath)
        save_path = os.path.join(current_app.root_path, "static", "img", filename)
      
        # folder存在確保
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 画像保存
        image = Image.open(file)
        image.save(save_path, quality=90)
        image_url = "/static/img/" + filename
        
         # DB操作
        con = connect_db()
        cur = con.cursor()
        
        sql = """
            UPDATE t_transaction 
            SET cleaningPhoto = %s , status=%s 
            WHERE id = %s
        """
        cur.execute(sql, (filename,"返送待ち",transaction_id))
    
        con.commit()
        cur.close()
        con.close()


        # Upload成功
        return render_template('deal/deal_detail.html', 
                             upload_success=True, 
                             image_url=image_url,
                             user_id=user_id,
                             transaction = transaction)
    
    except Exception as e:
        error = f"ファイルの保存に失敗しました: {str(e)}"
        return render_template('deal/deal_detail.html', 
                             upload_success=False, 
                             error=error, 
                             user_id=user_id)    
# received取引詳細の画像添付 ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/list/received/imageUpload/<int:transaction_id>', methods=['POST'])
def deal_list_received_imageUpload(transaction_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': '用戶未登入'}), 401
    
    user_id = session.get('user_id')
    
    if 'img' not in request.files or not request.files['img'].filename:
        return jsonify({'success': False, 'error': 'ファイルが選択されていません'}), 400
    
    file = request.files['img']

    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return jsonify({'success': False, 'error': '許可されていないファイル形式です'}), 400
    
    try:
        filename = secure_filename(file.filename)
        savedata = datetime.now().strftime("%Y%m%d%H%M%S_")
        filename = savedata + filename
        
        save_path = os.path.join(current_app.root_path, "static", "img", filename)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 保存
        image = Image.open(file)
        image.save(save_path, quality=90)
        image_url = "/static/img/" + filename
        
        # 操作
        con = connect_db()
        cur = con.cursor(dictionary=True)
        sql_check = """
            SELECT situation
            FROM t_transaction
            WHERE id = %s
        """
        cur.execute(sql_check,(transaction_id,))
        check = cur.fetchone()
        print(check)
        if check['situation'] == "購入":
            updateSituation = "取引完了"
        else:
            updateSituation = "レンタル中"
        print(updateSituation)
         
        sql = """
            UPDATE t_transaction 
            SET receivedPhoto = %s,status=%s 
            WHERE id = %s
        """
        cur.execute(sql, (filename, updateSituation ,transaction_id))
        
        con.commit()
        cur.close()
        con.close()
        
        # 返回成功回應
        return jsonify({
            'success': True,
            'message': 'アップロード成功',
            'image_url': image_url,
            'filename': filename
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'ファイルの保存に失敗しました: {str(e)}'
        }), 500
        
# 出品者 received取引詳細の画像添付 ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/list/returnReceived/imageUpload/<int:transaction_id>', methods=['POST'])
def deal_list_returnReceived_imageUpload(transaction_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': '用戶未登入'}), 401
    
    user_id = session.get('user_id')
    
    if 'img' not in request.files or not request.files['img'].filename:
        return jsonify({'success': False, 'error': 'ファイルが選択されていません'}), 400
    
    file = request.files['img']

    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return jsonify({'success': False, 'error': '許可されていないファイル形式です'}), 400
    
    try:
        filename = secure_filename(file.filename)
        savedata = datetime.now().strftime("%Y%m%d%H%M%S_")
        filename = savedata + filename
        
        save_path = os.path.join(current_app.root_path, "static", "img", filename)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 保存
        image = Image.open(file)
        image.save(save_path, quality=90)
        image_url = "/static/img/" + filename
        
        # 操作
        con = connect_db()
        cur = con.cursor(dictionary=True)
        
         
        sql = """
            UPDATE t_transaction 
            SET receivedPhoto = %s,status=%s 
            WHERE id = %s
        """
        cur.execute(sql, (filename, "取引完了" ,transaction_id))
        
        con.commit()
        cur.close()
        con.close()
        
        # 返回成功回應
        return jsonify({
            'success': True,
            'message': 'アップロード成功',
            'image_url': image_url,
            'filename': filename
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'ファイルの保存に失敗しました: {str(e)}'
        }), 500
        
# shipping取引詳細の画像添付 ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/list/shipping/imageUpload/<int:transaction_id>', methods=['POST'])
def deal_list_shipping_imageUpload(transaction_id):
    # euser検証成功
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    if 'img' not in request.files or not request.files['img'].filename:
        return jsonify({'success': False, 'error': 'ファイルが選択されていません'}), 400
    
    file = request.files['img']

    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return jsonify({'success': False, 'error': '許可されていないファイル形式です'}), 400
    
    try:
        # システム用的画像名を生成
        filename = secure_filename(file.filename)
        savedata = datetime.now().strftime("%Y%m%d%H%M%S_")
        filename = savedata + filename
        
        # 保存パス生成
        # current_filepath = os.path.abspath(__file__)
        # current_dictionary = os.path.dirname(current_filepath)
        save_path = os.path.join(current_app.root_path, "static", "img", filename)
      
        # folder存在確保
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 画像保存
        image = Image.open(file)
        image.save(save_path, quality=90)
        image_url = "/static/img/" + filename
         # DB操作
        con = connect_db()
        cur = con.cursor()
        
        sql = """
            UPDATE t_transaction 
            SET shippingPhoto = %s,status = %s 
            WHERE id = %s
        """
        cur.execute(sql, (filename,'配達中',transaction_id))
      
        con.commit()
     
        cur.close()
        con.close()

        # Upload成功
         # 返回成功
        return jsonify({
            'success': True,
            'message': 'アップロード成功',
            'image_url': image_url,
            'filename': filename
        }), 200
    except Exception as e:
        error = f"ファイルの保存に失敗しました: {str(e)}"
        return render_template('deal/deal_detail.html', 
                             upload_success=False, 
                             error=error, 
                             user_id=user_id)  

# Return shipping取引詳細の画像添付 ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/list/return/imageUpload/<int:transaction_id>', methods=['POST'])
def deal_list_return_imageUpload(transaction_id):
    # euser検証成功
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    if 'img' not in request.files or not request.files['img'].filename:
        return jsonify({'success': False, 'error': 'ファイルが選択されていません'}), 400
    
    file = request.files['img']

    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return jsonify({'success': False, 'error': '許可されていないファイル形式です'}), 400
    
    try:
        # システム用的画像名を生成
        filename = secure_filename(file.filename)
        savedata = datetime.now().strftime("%Y%m%d%H%M%S_")
        filename = savedata + filename
        
        # 保存パス生成
        # current_filepath = os.path.abspath(__file__)
        # current_dictionary = os.path.dirname(current_filepath)
        save_path = os.path.join(current_app.root_path, "static", "img", filename)
      
        # folder存在確保
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 画像保存
        image = Image.open(file)
        image.save(save_path, quality=90)
        image_url = "/static/img/" + filename
         # DB操作
        con = connect_db()
        cur = con.cursor()
        
        sql = """
            UPDATE t_transaction 
            SET shippingPhoto = %s,status = %s 
            WHERE id = %s
        """
        cur.execute(sql, (filename,'返送中',transaction_id))
      
        con.commit()
     
        cur.close()
        con.close()

        # Upload成功
         # 返回成功
        return jsonify({
            'success': True,
            'message': 'アップロード成功',
            'image_url': image_url,
            'filename': filename
        }), 200
    except Exception as e:
        error = f"ファイルの保存に失敗しました: {str(e)}"
        return render_template('deal/deal_detail.html', 
                             upload_success=False, 
                             error=error, 
                             user_id=user_id)  
                 
# 評価 ----------------------------------------------------------------------------------------------------------------------------------------------------------
@deal_bp.route('/evaluation', methods=['POST'])
def evaluation():
    data = request.json
    evaluation_rating = int(data.get('evaluation'))
    transaction_id = int(data.get('transaction_id'))
    user_id = session.get('user_id')
    
    # 検証
    if not evaluation_rating or not transaction_id:
        return {'error': '評価またはID が不足しています'}, 400

    try:
        # DB操作
        con = connect_db()
        cur = con.cursor()
        
        sql = """
            INSERT INTO t_evaluation (transaction_id, score, evaluationTime, recipient_id) 
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (transaction_id, evaluation_rating, datetime.now(), user_id))
    
        con.commit()
        cur.close()
        con.close()

        return {'success': True, 'message': '評価しました'}
    except Exception as e:
        return {'error': str(e)}, 500
# comment ----------------------------------------------------------------------------------------------------------------------------------------------------------
# 既に存在するcommentsの取り処理
@deal_bp.route('/get-comments', methods=['GET'])
def get_comments():
    # transaction_id = request.args.get('transaction_id')
    # user検証
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
        
    product_id = request.args.get('product_id')
    
    if not product_id:
        return jsonify({'success': False, 'message': 'transaction_id が必要です'}), 400
    
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        
        # t_commentsにいるコメント
        sql = """
            SELECT 
                t.account_id,
                t.content,
                t.createdDate,
                t.product_id,
                a.firstName
            FROM t_comments t
            LEFT JOIN m_account a
            ON t.account_id = a.id
            WHERE t.product_id = %s
            ORDER BY t.createdDate DESC
        """
        cur.execute(sql, (product_id,))
        comments = cur.fetchall()
       
        cur.close()
        con.close()
        
        # datetimeを文字列に変換しないとjsonが読めない
        comments_list = []
        for comment in comments:
            comments_list.append({
                'account_id': comment['account_id'],
                'firstName': comment['firstName'] or '匿名',  # 名前がなければ
                'content': comment['content'],
                'createdDate': comment['createdDate'].isoformat() if comment['createdDate'] else None  #date型→str
            })
        return jsonify(comments_list), 200
    
    except Exception as e:
        print(f'Error getting comments: {str(e)}')
        return jsonify({'success': False, 'message': str(e)}), 500


# 新しい comment　提出
@deal_bp.route('/add-comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'ログインが必要です'}), 401
    
    user_id = session.get('user_id')
    data = request.get_json()
    
    product_id = data.get('product_id')
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'success': False, 'message': 'コメントを入力してください'}), 400
    
    try:
        con = connect_db()
        cur = con.cursor()
        
        #  comment　→　DB
        sql = """
            INSERT INTO t_comments ( product_id, account_id, content, createdDate)
            VALUES ( %s, %s, %s, %s)
        """
        
        cur.execute(sql, (
            product_id,
            user_id,
            content,
            datetime.now()
        ))
        
        con.commit()
        comment_id = cur.lastrowid    #AUTO INCREMENTの値を取得
        
        cur.close()
        con.close()
        
        return jsonify({
            'success': True,
            'message': 'コメントを送信しました',
            'comment_id': comment_id
        }), 200
    
    except Exception as e:
        print(f'Error adding comment: {str(e)}')
        return jsonify({'success': False, 'message': str(e)}), 500

#DB設定------------------------------------------------------------------------------------------------------------------------------------------------------------------
def connect_db():
    con=mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = '',
        db ='db_subkari'
    )
    return con