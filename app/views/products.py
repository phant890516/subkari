from flask import Blueprint, render_template, request, make_response, session, redirect, url_for
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import mysql.connector
import json
import os
import random



# Blueprintの設定
products_bp = Blueprint('products', __name__, url_prefix='/products')


#プロフィールに表示する取引情報を取得する ------------------------------------------------------------------------------------
#引数として受け取ったidを持つユーザーの情報を取得
def get_transaction_info(id):
    #アカウントテーブルからは取れない情報を取得
    con = connect_db()
    cur = con.cursor(dictionary=True)
      
    #フォロワー数、フォロー数、評価、総評価件数、出品数を取得
    #フォロー数
    sql="select count(*) as フォロー数 from t_connection where execution_id=%s and type='フォロー' group by execution_id"
    cur.execute(sql, (id,))
    follows=cur.fetchone()
    #フォロワー数
    sql="select count(*) as フォロワー数 from t_connection where target_id=%s and type='フォロー' group by target_id"
    cur.execute(sql, (id,))
    followers=cur.fetchone()
    #評価
    sql="select avg(score) as 評価 from t_evaluation where recipient_id=%s group by recipient_id"
    cur.execute(sql, (id,))
    evaluation=cur.fetchone()
    #総評価件数
    sql="select count(*) as 評価件数 from t_evaluation where recipient_id=%s group by recipient_id"
    cur.execute(sql, (id,))
    evaluationCount=cur.fetchone()
    #出品数
    sql="select count(*) as 出品数 from m_product where account_id=%s"
    cur.execute(sql, (id,))
    products=cur.fetchone()
    #評価を変形
    if evaluation is not None:
        evaluation=round(float(evaluation['評価']))     #小数点型にしてから四捨五入
    else:
        evaluation = 0
        evaluationCount = {"評価件数":0}
    return evaluation,evaluationCount


#引数として受け取ったidを持つユーザーの情報を取得
def get_user_info(id):
    sql = "SELECT * FROM m_account WHERE id = %s"
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql, (id,))  # ← タプルで渡す！
    user_info = cur.fetchone()
    return user_info



#アカウントの口座情報を取得する ------------------------------------------------------------------------------
def getAccountInfo():
    accountNumbers=[]                 #口座番号下位三桁を格納
    id=session["user_id"]
    con=connect_db()
    cur=con.cursor(dictionary=True)
    sql="select bankName,accountNumber,branchCode from t_transfer  where account_id=%s limit 3"
    cur.execute(sql,(id,))
    bank_info=cur.fetchall()
    cur.close()
    con.close()
    count=0
    #口座がいくつ登録されているかを数える
    for i in bank_info:
        count+=1

    #口座番号マスク処理のために口座番号の桁数と下位三桁を抽出し配列に入れる
    for i in range(count):
        num=int(bank_info[i]['accountNumber'])

        tmp=num
        length=0
        mask=""
        #口座番号の桁数を取得
        while tmp>0:
            tmp=tmp//10
            length+=1
        for i in range(length-3):
        
            mask+="*"

        num=str(num%1000)
        num=mask+num                #マスク処理を施した口座番号
        accountNumbers.append(num)
    return accountNumbers,count

#商品情報を取得する ------------------------------------------------------------------------------------
def get_product_info(product_id):
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        # 商品情報を取得
        sql_product = """
        SELECT 
        pr.id ,
        pr.name as product_name,
        pr.account_id, 
        pr.rentalPrice, 
        pr.purchasePrice, 
        pr.explanation ,
        pr.color,
        pr.for,
        pr.category_id,
        pr.brand_id ,
        br.name as brand_name  , 
        ca.name as category_name,
        pr.purchaseFlg,
        pr.rentalFlg,
        pr.rentalPeriod,
        pr.condition
        

        FROM m_product pr
        INNER JOIN m_brand br ON br.id = pr.brand_id
        INNER JOIN m_category ca ON pr.category_id = ca.id
        WHERE pr.id = %s;
        """
        cur.execute(sql_product, (product_id,))
        product = cur.fetchone()
        return product
    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
        return None
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()



#レンタル情報を計算する関数 ------------------------------------------------------------------------------------
def calculate_rental_price(product_id):

    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        # 商品情報を取得
        product = get_product_info(product_id)

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()

    # 2. 期間ごとの合計金額を計算し、辞書として保存する
    calculated_prices = {}

    # 1. レンタル単価を取得（数値型に変換）
    if( product['rentalFlg'] == 0):
        rental_price_per_day = 0
    else:
        try:
            # product.rentalPrice は文字列の可能性もあるため、int型に変換
            rental_price_per_day = int(product['rentalPrice'])
            #データを入れるperiod_stringに      
            period_string = product['rentalPeriod']
            # '日' という文字を空文字に置き換え（例: '4日' -> '4'）
            days_str = period_string

            days = int(days_str)
        
            # 計算
            total_price = rental_price_per_day * days
        
            # 結果を辞書に追加
            # 例: {'4日': 4000, '7日': 7000} のように格納
            calculated_prices[f'{days}日'] = total_price
        except (TypeError, ValueError):
            # エラーハンドリング: 価格が不正な場合は0としておくなど
            pass

    return calculated_prices
            


#コメントの情報を取得する関数 ------------------------------------------------------------------------------------
def get_comments(product_id):
    # 2. コメントデータと投稿者名を取得
        # t_comments と m_account を結合し、投稿日時の降順で取得
    comments = []  # コメントリストを初期化
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        # 商品情報を取得
        product = get_product_info(product_id)



        sql_comments = """
            SELECT 
                t.content AS text, 
                m.username AS user_name, 
                t.account_id AS comment_acouunt_id,
                t.createdDate

            FROM 
                t_comments t
            JOIN 
                m_account m ON t.account_id = m.id
            WHERE 
                t.product_id = %s
            ORDER BY 
                t.createdDate ASC;
        """

        cur.execute(sql_comments, (product_id,))
        fetched_comments = cur.fetchall()

        
        # 3. HTMLテンプレートに渡す形式にデータを整形
        # 商品の出品者IDと比較して、出品者かどうかを判定するフラグを追加
        seller_id = product['account_id'] # m_productから取得した出品者のaccount_id
        
        for comment in fetched_comments:
            is_seller = (comment['comment_acouunt_id'] == seller_id)
            
            # テンプレートに渡すコメントリストに追加
            comments.append({
                'user_name': comment['user_name'],
                'text': comment['text'],
                'is_seller': is_seller,
                # 日付も表示したい場合はここで整形して渡すことも可能
                'created_date': comment['createdDate'].strftime('%Y/%m/%d %H:%M') if comment['createdDate'] else ''
            })
    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()
    return comments

#トップサイズ情報を取得する関数 ------------------------------------------------------------------------------------
def get_topsSize(product_id):
    topsSize = None
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        sql_topSize ="""
        SELECT
        shoulderWidth ,bodyWidth , sleeveLength , bodyLength , notes
        from
        m_topsSize
        where
        product_id = %s;
        """
        cur.execute(sql_topSize, (product_id,))
        topsSize = cur.fetchone()
    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()
    return topsSize

#ボトムスサイズ情報を取得する関数 ------------------------------------------------------------------------------------
def get_bottomsSize(product_id):
    bottomsSize = None
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        sql_bottomsSize = """
        SELECT
        hip 
        , totalLength 
        , rise 
        , inseam 
        , waist 
        , thighWidth 
        , hemWidth 
        , skirtLength
        , notes

        from
        m_bottomsSize

        where
        product_id = %s;
        """
        cur.execute(sql_bottomsSize, (product_id,))
        bottomsSize = cur.fetchone()
    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()
    return bottomsSize


#商品写真のデータを取得する関数 ------------------------------------------------------------------------------------
def get_product_images(product_id):
        
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        
        #商品画像
        sql_images = """
            SELECT img
            FROM m_productimg
            WHERE product_id = %s;
        """
        cur.execute(sql_images,(product_id,))
        images = cur.fetchall()
    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
        images = []
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()

    return images

#出品者の他の商品写真を取得する関数 ------------------------------------------------------------------------------------
def get_other_products_images(seller_id , current_product_id):
        
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        
        #同じ出品者の他の商品画像
        sql_images = """
            SELECT
                p.id AS product_id,
                p.name AS product_name,
                p.purchasePrice,
                p.rentalPrice,
                p.condition,
                pi_main.img AS first_image
            FROM
                m_product AS p
            INNER JOIN
                m_productImg AS pi_main ON p.id = pi_main.product_id
            LEFT JOIN
                m_productImg AS pi_prev ON p.id = pi_prev.product_id AND pi_prev.id < pi_main.id
            WHERE
                pi_prev.id IS NULL           
                AND p.account_id = %s        -- 出品者IDで絞り込み
                AND p.id != %s               -- 現在の商品を除外
                AND p.showing = '公開'       -- 公開中の商品のみ
                AND p.`condition` = '取引可'  -- 取引可能な商品に限定
            ORDER BY
                p.updateDate DESC;
        """
        cur.execute(sql_images,(seller_id , current_product_id))
        other_products_images = cur.fetchall()
    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
        other_products_images = []
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()

    return other_products_images


#おすすめの商品をランダムに取得する関数 ------------------------------------------------------------------------------------
def get_recommended_products(current_product_id, limit=4):
    """
    color, for, brand_id, category_id の中から、ランダムに一つだけ条件を選んでおすすめ商品を取得する。
    """
    
    # --- 1. 現在の商品の情報を取得 ---
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        
        sql_current = """
            SELECT brand_id, category_id, color, `for`, account_id 
            FROM m_product 
            WHERE id = %s;
        """
        cur.execute(sql_current, (current_product_id,))
        current_product = cur.fetchone()
        
        if not current_product:
            return [], "商品情報が見つかりません" 
            
    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
        return [], "DBエラー"
    finally:
        if 'con' in locals() and con and con.is_connected():
            # DB接続を閉じる前にカーソルを閉じる
            if 'cur' in locals() and cur:
                cur.close()
            con.close()


    # --- 2. 検索ロジックをランダムに決定（どれか一つだけ） ---
    
    # 候補となる条件を辞書で定義 (値がNoneでないもののみ)
    conditions = {}
    if current_product['brand_id']: conditions['brand_id'] = current_product['brand_id']
    if current_product['category_id']: conditions['category_id'] = current_product['category_id']
    if current_product['color']: conditions['color'] = current_product['color']
    if current_product['for']: conditions['for'] = current_product['for']
    
    where_clauses = []
    params = []
    
    if not conditions:
        # すべての条件がNULLの場合
        logic_name = "条件なし（ランダム）"
        where_clauses.append("p.account_id != %s") # 自出品者を除外
        params.append(current_product['account_id'])
    else:
        # 有効な条件の中から一つだけランダムに選ぶ
        chosen_key = random.choice(list(conditions.keys()))
        chosen_value = conditions[chosen_key]
        
        # SQLのWHERE句とパラメータを設定
        where_clauses.append(f"p.{chosen_key} = %s")
        params.append(chosen_value)
        
        # HTML表示用の条件名を生成
        display_name = {
            'brand_id': 'ブランド',
            'category_id': 'カテゴリ',
            'color': 'カラー',
            'for': '対象'
        }.get(chosen_key, chosen_key)
        
        logic_name = f"{display_name} ({chosen_value}) が一致"

        # 現在の商品IDを除外
        where_clauses.insert(0, "p.id != %s")
        params.insert(0, current_product_id)


    # --- 3. データベースを検索して商品を取得 ---
    
    where_sql = " AND ".join(where_clauses)
    
    # 最初の画像を取得する効率的なSQLを組み合わせる
    sql_recommendations = f"""
        SELECT
            p.id AS product_id,
            p.name,
            p.purchasePrice,
            p.rentalPrice,
            pi_main.img AS first_image,
            p.purchaseFlg,
            p.rentalFlg
        FROM
            m_product AS p
        INNER JOIN
            m_productImg AS pi_main ON p.id = pi_main.product_id
        LEFT JOIN
            m_productImg AS pi_prev ON p.id = pi_prev.product_id AND pi_prev.id < pi_main.id
        WHERE
            pi_prev.id IS NULL
            AND p.showing = '公開'
            AND p.condition = '取引可'
            AND {where_sql}
        ORDER BY
            RAND()
        LIMIT %s;
    """
    params.append(limit)

    try:
        # 再度DB接続
        con = connect_db()
        cur = con.cursor(dictionary=True)

        cur.execute(sql_recommendations, tuple(params))
        recommended_products = cur.fetchall()

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
        recommended_products = []
        
    finally:
        if 'con' in locals() and con and con.is_connected():
            if 'cur' in locals() and cur:
                cur.close()
            con.close()
            
    return recommended_products, logic_name


#コネクション情報取得関数 ------------------------------------------------------------------------------------
def get_connection(target_id):

    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        connection_sql = """
            SELECT * FROM t_connection WHERE execution_id = %s AND target_id = %s AND type = 'フォロー';
        """
        cur.execute(connection_sql, (session['user_id'],target_id))
        connection = cur.fetchone()

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
        connection = None
    finally:
        if con and con.is_connected():
            cur.close()
            con.close()
    return connection

    

# 商品一覧の表示
@products_bp.route('/search_result', methods=['GET'])
def search_result():
    user_id = session.get('user_id')
    products = []

    # DBに接続して商品情報を取得
    con = None
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)  # 辞書形式で取得
        sql = "SELECT id, name, brand, price, image_path FROM m_product LIMIT 50;"
        cur.execute(sql)
        products = cur.fetchall()
        cur.close()
    except mysql.connector.Error as err:
        print(f"DB Error: {err}")
    finally:
        if con and con.is_connected():
            con.close()

    # 'top/search_product.html' テンプレートをレンダリングし、商品リストを渡す
    resp = make_response(render_template(
        'top/search_product.html',
        user_id=user_id,
        products=products
    ))
    return resp

# 商品詳細の表示
@products_bp.route('/<int:product_id>', methods=['GET'])
def product_details_stub(product_id):
    # sessionからuser_idを取得
    user_id = session.get('user_id')

    product = None
    comments = []  # コメントリストを初期化
    con = None
    cur = None

    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        # 商品情報を取得
        product = get_product_info(product_id)
        
        #商品画像の情報を取得
        images = get_product_images(product_id)
        # sql_images = """
        #     SELECT img
        #     FROM m_productimg
        #     WHERE product_id = %s;
        # """
        # cur.execute(sql_images,(product_id,))
        # images = cur.fetchall()
        # print(images)
        #images=["img":"image1.png","img":"image2.png",...]

        #商品が見つからない場合の処理
        # sql_img = """
        #     SELECT
        # """
        # 商品が見つからなかった場合のデフォルト処理
        # ... 省略 ...
        if not product:

            
            # 商品が見つからない場合は、エラーページや404を返すのが適切です
            return render_template('error.html'), 404 # **ここで関数を終了させる**

        # #--レンタル期間情報を取得--

        
    
        # コメント情報を取得
        # 2. コメントデータと投稿者名を取得
        # t_comments と m_account を結合し、投稿日時の降順で取得
        sql_comments = """
            SELECT 
                t.content AS text, 
                m.username AS user_name, 
                t.account_id AS comment_acouunt_id,
                t.createdDate

            FROM 
                t_comments t
            JOIN 
                m_account m ON t.account_id = m.id
            WHERE 
                t.product_id = %s
            ORDER BY 
                t.createdDate ASC;
        """

        cur.execute(sql_comments, (product_id,))
        fetched_comments = cur.fetchall()

        
        # 3. HTMLテンプレートに渡す形式にデータを整形
        # 商品の出品者IDと比較して、出品者かどうかを判定するフラグを追加
        seller_id = int(product['account_id']) # m_productから取得した出品者のaccount_id
        
        for comment in fetched_comments:
            is_seller = (comment['comment_acouunt_id'] == seller_id)
            
            # テンプレートに渡すコメントリストに追加
            comments.append({
                'user_name': comment['user_name'],
                'text': comment['text'],
                'is_seller': is_seller,
                # 日付も表示したい場合はここで整形して渡すことも可能
                'created_date': comment['createdDate'].strftime('%Y/%m/%d %H:%M') if comment['createdDate'] else ''
            })

        #トップサイズ情報を取得
        sql_topSize ="""
        SELECT
        shoulderWidth ,bodyWidth , sleeveLength , bodyLength , notes
        from
        m_topsSize
        where
        product_id = %s;
        """
        cur.execute(sql_topSize, (product_id,))
        topSize = cur.fetchone()


        #ボトムスサイズ情報を取得
        sql_bottomsSize = """
        SELECT
        hip 
        , totalLength 
        , rise 
        , inseam 
        , waist 
        , thighWidth 
        , hemWidth 
        , skirtLength
        , notes

        from
        m_bottomsSize

        where
        product_id = %s;
        """
        cur.execute(sql_bottomsSize, (product_id,))
        bottomsSize = cur.fetchone()


       
    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")

    finally:
        if con and con.is_connected():
            cur.close()
            con.close()


    #レンタル価格計算
    calculated_prices = calculate_rental_price(product_id)


    # 評価情報を取得
    evaluation, evaluationCount = get_transaction_info(product['account_id'])

    #アカウント情報取得
    seller_info = get_user_info(product['account_id'])

    erroer_message = ""

    #出品者の他の商品画像を取得
    other_products_images = get_other_products_images(seller_id=product['account_id'] , current_product_id=product_id)
    
    #おすすめ商品を取得
    recommended_products, logic_name= get_recommended_products(product_id)

    #コネクション情報取得
    if user_id:
        connection = get_connection(product['account_id'])
    else:
        connection = None
    
    

    # 取得した商品情報 (product) とコメント (comments) をテンプレートに渡す
    resp = make_response(render_template(
        'products/product_details.html',
        evaluationCount=evaluationCount['評価件数'],
        user_id=user_id,
        seller_info=seller_info,
        connection=connection,
        product=product,
        images = images,
        other_products_images=other_products_images,
        comments=comments,
        calculated_prices = calculated_prices,
        evaluation=evaluation,
        topSize=topSize,
        bottomsSize=bottomsSize,
        recommended_products=recommended_products,
        logic_name=logic_name,
        error_message=erroer_message
    ))
    return resp

#コメント送信処理
@products_bp.route('/submit_comment/<int:product_id>', methods=['POST'])
def submit_comment(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    user_id = session.get('user_id')
    comment_text = request.form.get('comment_text')

    if not comment_text:
        return redirect(url_for('products.product_details_stub', product_id=product_id))

    # コメントをデータベースに保存
    try:
        con = connect_db()
        cur = con.cursor()

        sql_insert = """
            INSERT INTO t_comments (product_id, account_id, content)
            VALUES (%s, %s, %s);
        """
        cur.execute(sql_insert, (product_id, user_id, comment_text))
        con.commit()

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")

    finally:
        if con and con.is_connected():
            cur.close()
            con.close()

    return redirect(url_for('products.product_details_stub', product_id=product_id))

#フォロー処理
@products_bp.route('/follow/<int:seller_id>', methods=['POST'])
def follow(seller_id):
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    user_id = session.get('user_id')

    try:
        con = connect_db()
        cur = con.cursor()

        # フォロー関係を挿入
        sql_follow = """
            INSERT INTO t_connection (execution_id, target_id, type)
            VALUES (%s, %s, 'フォロー');
        """
        cur.execute(sql_follow, (user_id, seller_id))
        con.commit()

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")

    finally:
        if con and con.is_connected():
            cur.close()
            con.close()

    return redirect(request.referrer or url_for('products.product_details_stub', product_id=0))


#purchase
#購入選択画面 レンタルと似た処理なので修正するときはこっちも修正すること
@products_bp.route('/purchase/<int:product_id>', methods=['GET'])
def purchase(product_id):
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    product = get_product_info(product_id)

    if not product:
        # 商品が見つからない場合は、エラーページや404を返すのが適切です
        return render_template('error.html'), 404 # **ここで関数を終了させる**
    if product['condition'] == '取引中' or product['condition'] == '売却済み':
        return render_template('error.html'), 404 # **ここで関数を終了させる**
    

    #共通処理
    #商品画像の情報を取得
    images = get_product_images(product_id)

    if product['purchaseFlg'] == 0:

        return redirect(url_for('products.product_details_stub', product_id=product_id))

        
        # # 評価情報を取得
        # evaluation, evaluationCount = get_transaction_info(product['account_id'])

        # #アカウント情報取得
        # seller_info = get_user_info(product['account_id'])

        # #コメント情報を取得
        # comments = get_comments(product_id)

        # #レンタル価格計算
        # calculated_prices = calculate_rental_price(product_id)

        # #--トップサイズ情報を取得--
        # topSize = get_topsSize(product_id)

        # #--ボトムスサイズ情報を取得--
        # bottomsSize = get_bottomsSize(product_id)

        

        # erroer_message = "この商品は購入できません。"

        # #出品者の他の商品画像を取得
        # other_products_images = get_other_products_images(seller_id=product['account_id'] , current_product_id=product_id)
    
        # #おすすめ商品を取得
        # recommended_products, logic_name= get_recommended_products(product_id)



        # # 購入不可の商品に対して購入ページにアクセスした場合の処理
        # return render_template('product_details.html',evaluationCount=evaluationCount['評価件数'],
        # evaluationCount=evaluationCount['評価件数'],
        # user_id=user_id,
        # seller_info=seller_info,
        # product=product,
        # images = images,
        # other_products_images=other_products_images,
        # comments=comments,
        # calculated_prices = calculated_prices,
        # evaluation=evaluation,
        # topSize=topSize,
        # bottomsSize=bottomsSize,
        # recommended_products=recommended_products,
        # logic_name=logic_name,
        # error_message=erroer_message
        # ), 404 # **ここで関数を終了させる**

    #DBから情報を取得
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        # # 商品情報を取得
        # sql_product = """
        # SELECT pr.id , pr.name as product_name,pr.account_id, pr.rentalPrice, pr.purchasePrice, pr.explanation ,pr.color,pr.for,pr.category_id,pr.brand_id ,br.name as brand_name  , ca.name as category_name
        # FROM m_product pr
        # INNER JOIN m_brand br ON br.id = pr.brand_id
        # INNER JOIN m_category ca ON pr.category_id = ca.id
        # WHERE pr.id = %s;
        # """
        # cur.execute(sql_product, (product_id,))
        # product = cur.fetchone()
        #配送情報を取得

        sql_address="""
        SELECT id,zip,pref,address1,address2,address3
        FROM m_address
        WHERE account_id = %s;
        """
        cur.execute(sql_address, (user_id,))
        address_list = cur.fetchall()


        #カード情報を取得
        sql_card="""
        SELECT id,number,expiry,holderName
        FROM t_creditCard
        WHERE account_id = %s;
        """
        cur.execute(sql_card, (user_id,))
        card_info = cur.fetchall()

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")

    finally:
        if con and con.is_connected():
            cur.close()
            con.close()
        
    #支払い情報を取得
    accountNumbers,count=getAccountInfo()

    return render_template("purchase/purchase.html",images = images ,user_id = user_id, product = product, address_list=address_list, card_info=card_info, accountNumbers=accountNumbers, count=count)

#レンタルができるようにする/購入と似た処理なので修正するときは注意
@products_bp.route('/rental/<int:product_id>', methods=['GET'])
def rental(product_id):
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    #商品情報を取得
    product = get_product_info(product_id)
    if not product:
        # 商品が見つからない場合は、エラーページや404を返すのが適切です
        return render_template('error.html'), 404 # **ここで関数を終了させる**
    
    if product['condition'] == '取引中' or product['condition'] == '売却済み':

        return render_template('error.html'), 404 # **ここで関数を終了させる**

    #共通処理
    #商品画像の情報を取得
    images = get_product_images(product_id)

    if product['rentalFlg'] == 0:

        return redirect(url_for('products.product_details_stub', product_id=product_id))

        # # 評価情報を取得
        # evaluation, evaluationCount = get_transaction_info(product['account_id'])

        # #アカウント情報取得
        # seller_info = get_user_info(product['account_id'])

        # #コメント情報を取得
        # comments = get_comments(product_id)

        # #レンタル価格計算
        # calculated_prices = calculate_rental_price(product_id)

        # #--トップサイズ情報を取得--
        # topSize = get_topsSize(product_id)

        # #--ボトムスサイズ情報を取得--
        # bottomsSize = get_bottomsSize(product_id)

        # erroer_message = "この商品はレンタルできません。"

        # #出品者の他の商品画像を取得
        # other_products_images = get_other_products_images(seller_id=product['account_id'] , current_product_id=product_id)
    
        # #おすすめ商品を取得
        # recommended_products, logic_name= get_recommended_products(product_id)



        
        # # 購入不可の商品に対して購入ページにアクセスした場合の処理
        # return render_template('product_details.html',evaluationCount=evaluationCount['評価件数'],
        # evaluationCount=evaluationCount['評価件数'],
        # user_id=user_id,
        # seller_info=seller_info,
        # product=product,
        # images = images,
        # other_products_images=other_products_images,
        # comments=comments,
        # calculated_prices = calculated_prices,
        # evaluation=evaluation,
        # topSize=topSize,
        # bottomsSize=bottomsSize,
        # recommended_products=recommended_products,
        # logic_name=logic_name,
        # error_message=erroer_message
        # ), 404 # **ここで関数を終了させる**

    #DBから情報を取得
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        #配送情報を取得
        sql_address="""
        SELECT id,zip,pref,address1,address2,address3
        FROM m_address
        WHERE account_id = %s;
        """
        cur.execute(sql_address, (user_id,))
        address_list = cur.fetchall()


        #カード情報を取得
        sql_card="""
        SELECT id,number,expiry,holderName
        FROM t_creditCard
        WHERE account_id = %s;
        """
        cur.execute(sql_card, (user_id,))
        card_info = cur.fetchall()

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")

    finally:
        if con and con.is_connected():
            cur.close()
            con.close()

    # #--レンタル期間情報を取得--

    #レンタル価格計算
    calculated_prices = calculate_rental_price(product_id)
        
    #支払い情報を取得
    accountNumbers,count=getAccountInfo()

    return render_template("purchase/rental.html",
    user_id = user_id,
    product = product,
    images = images ,
    address_list=address_list, 
    card_info=card_info,
    accountNumbers=accountNumbers, 
    count=count ,
    calculated_prices=calculated_prices)







#購入・レンタル完了画面
@products_bp.route('/transaction_complete', methods=['POST'])
def transaction_complete():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    product_id = request.form.get('product_id')
    payment_method = request.form.get('payment_method')
    addressId = request.form.get('address_index')
    delivery_location = request.form.get('delivery_location')
    creditcard_id = request.form.get('creditcard_id')
    situation = request.form.get('situation')


    # print("product_id:",product_id)
    print("payment_method:",payment_method)
    # print("addressId:",addressId)
    # print("delivery_location:",delivery_location)
    # print("creditcard_id:",creditcard_id)


    #購入項目があるかチェック
    if payment_method =="クレジットカード":
        if not product_id or not payment_method or not addressId or not delivery_location or not creditcard_id:

                
            # 商品が見つからない場合は、エラーページや404を返すのが適切です
            return render_template('error.html'), 404 # **ここで関数を終了させる**
    else:
        if not product_id or not payment_method or not addressId or not delivery_location:

                
            # 商品が見つからない場合は、エラーページや404を返すのが適切です
            return render_template('error.html'), 404 # **ここで関数を終了させる**

    #payment_methodがクレジットならpayment_methodを発送待ちにする
    if payment_method == "クレジットカード":
        status = "発送待ち"
        paymentDeadline = None
        creditcard_id = int(creditcard_id)
    else:
        status = "支払い待ち"
        #72時間後の日付を取得
        paymentDeadline = datetime.now() + timedelta(hours=72)
        creditcard_id = None

    #商品情報を取得
    product = get_product_info(product_id)

    # get_product_info()で取得した商品の販売者ID
    seller_id = product['account_id']
    addressId = int(addressId)

    #預かり書と発送書のフラグ
    shipping_flg = False
    received_flg = False

    
    # dbへの登録処理
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)

        #住所情報を取得
        sql_address="""
        SELECT
        pref,address1,address2,address3
        FROM m_address
        WHERE id = %s;
        """
        cur.execute(sql_address, (addressId,))
        address = cur.fetchone()
        shippingAddress = f"{address['pref']} {address['address1']} {address['address2']} {address['address3']}"

        

        #購入情報をt_purchaseテーブルに登録
        sql_purchase="""
        INSERT INTO t_transaction (
        customer_id,
        seller_id, 
        product_id, 
        status,
        situation,
        paymentMethod,
        paymentDeadline,
        shippingAddress,
        creditcard_id,
        shippingFlg,
        receivedFlg)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s);
        """
        #situation #取引状態・購入の場合は'購入'レンタルの場合は'レンタル'
        cur.execute(sql_purchase, (user_id, seller_id, product_id, status,situation,payment_method,paymentDeadline, shippingAddress, creditcard_id,shipping_flg,received_flg))
        con.commit()

        # 商品テーブルを更新
        sql_update_product="""
        UPDATE m_product
        SET `condition` = '取引中'
        WHERE id = %s;
        """
        cur.execute(sql_update_product, (product_id,))
        con.commit()



        

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")

    finally:
        if con and con.is_connected():
            cur.close()
            con.close()

    return render_template("purchase/transaction_complete.html", user_id=user_id)


#レンタル完了画面
@products_bp.route('/rental_complete', methods=['POST'])
def rental_complete():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

        

    return render_template("purchase/rental_complete.html", user_id=user_id)

# DB接続設定
def connect_db():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        db='db_subkari'
    )
    return con

