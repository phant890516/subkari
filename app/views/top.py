from flask import Blueprint, render_template, request, make_response, redirect, url_for, session
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime , timedelta
import mysql.connector
import math
import json
import os


# /app/views/top.py のファイルの先頭に追加
top_bp = Blueprint('top', __name__)



# =======================================================================
#  修正点: 50件のダミー商品データと画像パスを定義
# =======================================================================

# 50枚のダミー画像パスを定義 (static/img/product_01.jpg から product_50.jpg を想定)
IMAGE_PATHS = [f'product_{i:02d}.jpg' for i in range(1, 51)]

# 50件分のダミー商品データ (5列 x 10行 = 50件)
DUMMY_PRODUCTS = [
    {
        'id': i, 
        'brand': ['TRAVAS TOKYO', 'REFLEM', 'CIVARIZE', 'LIZ LISA', 'KINGLYMASK'][i % 5],
        'name': f'商品名サンプル {i:02d}',
        'price': 1500 + (i * 100) % 5000, 
        # 50個の異なる画像パスを使用
        'image_path': IMAGE_PATHS[i] 
    } 
    for i in range(40) 
]

# =======================================================================
# 訪客のtop page表示
# =======================================================================
@top_bp.route('/')
def guest_index():
    if 'user_id' in session:
        user_id = session.get('user_id')
        # エンドポイントは 'top.member_index'
        resp = make_response(redirect(url_for('top.member_index')))
    else :
        user_id = None
    
    con = connect_db()
    cur = con.cursor(dictionary=True)

    # すべての商品を取り出し
    sql = """
        SELECT 
            p.id,
            p.name,
            p.rentalPrice,
            p.purchasePrice,
            c.name AS category,
            b.name AS brand,
            (
                SELECT m2.img 
                FROM m_productimg AS m2
                WHERE m2.product_id = p.id
                ORDER BY m2.id ASC
                LIMIT 1
            ) AS image_path
        FROM m_product AS p
        LEFT JOIN m_brand AS b ON p.brand_id = b.id
        LEFT JOIN m_category AS c ON p.category_id = c.id
        WHERE p.draft = 0
        GROUP BY p.id
        ORDER BY p.category_id, p.id
    """
    cur.execute(sql)
    rows = cur.fetchall()

    #  KEY is category の辞書
    categories = {}
    for row in rows:
        rental = row.get("rentalPrice")
        purchase = row.get("purchasePrice")

        # 価格表示の決定
        if rental is not None and purchase is not None:
            price_text = f"{rental:,} / {purchase:,}"
        elif rental is not None:
            price_text = f"{rental:,}"
        elif purchase is not None:
            price_text = f"{purchase:,}"
        else:
            price_text = "ー"

        # 分類
        cat = row["category"] or "その他"
        if cat not in categories:
            categories[cat] = []
        if len(categories[cat]) < 4:
            categories[cat].append({
            "id": row["id"],
            "name": row["name"],
            "brand": row["brand"] or "",
            "price": price_text,
            "image_path": row["image_path"] or "default.png"
            })

    cur.close()
    con.close()
    print(categories)
    return render_template('top/guest_index.html', user_id = user_id,  categories=categories)

# 会員のtop page表示
@top_bp.route('/top',methods=['GET'])
def member_index():
    if 'user_id' not in session:
        # エンドポイントは 'login.login'
        resp = make_response(url_for('login.login'))
        user_id = None
    else:
        user_id = session.get('user_id')
        
    con = connect_db()
    cur = con.cursor(dictionary=True)

    # すべての商品を取り出し
    sql = """
        SELECT 
            p.id,
            p.name,
            p.rentalPrice,
            p.purchasePrice,
            c.name AS category,
            b.name AS brand,
            (
                SELECT m2.img 
                FROM m_productimg AS m2
                WHERE m2.product_id = p.id
                ORDER BY m2.id ASC
                LIMIT 1
            ) AS image_path
        FROM m_product AS p
        LEFT JOIN m_brand AS b ON p.brand_id = b.id
        LEFT JOIN m_category AS c ON p.category_id = c.id
        WHERE p.draft = 0
        GROUP BY p.id
        ORDER BY p.category_id, p.id
    """
    cur.execute(sql)
    rows = cur.fetchall()

    #  KEY is category の辞書
    categories = {}
    for row in rows:
        rental = row.get("rentalPrice")
        purchase = row.get("purchasePrice")

        # 価格表示の決定
        if rental is not None and purchase is not None:
            price_text = f"{rental:,} / {purchase:,}"
        elif rental is not None:
            price_text = f"{rental:,}"
        elif purchase is not None:
            price_text = f"{purchase:,}"
        else:
            price_text = "ー"

        # 分類
        cat = row["category"] or "その他"
        if cat not in categories:
            categories[cat] = []
        if len(categories[cat]) < 4:
            categories[cat].append({
            "id": row["id"],
            "name": row["name"],
            "brand": row["brand"] or "",
            "price": price_text,
            "image_path": row["image_path"] or "default.png"
            })

    cur.close()
    con.close()

    return render_template("top/member_index.html", categories=categories ,user_id = user_id)

#categoryによるの商品一覧
@top_bp.route('/category/<category>',methods=['GET'])
def category_products(category):
    if 'user_id' not in session:
        # エンドポイントは 'login.login'
        resp = make_response(url_for('login.login'))
        user_id = None
    else:
        user_id = session.get('user_id')
    
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            p.id,
            p.name,
            p.rentalPrice,
            p.purchasePrice,
            b.name AS brand,
            c.name AS category,
             (
                SELECT m2.img 
                FROM m_productimg AS m2
                WHERE m2.product_id = p.id
                ORDER BY m2.id ASC
                LIMIT 1
            ) AS image_path
        FROM 
            m_product AS p
        LEFT JOIN 
            m_brand AS b ON p.brand_id = b.id
        LEFT JOIN 
            m_category AS c ON p.category_id = c.id
        WHERE 
            c.name = %s
        AND
            p.draft = 0
        ORDER BY 
            p.id DESC
    """, (category,))
    rows = cur.fetchall()
    cur.close()
    con.close()

    # ひとつのカテゴリのみ---
    categories = {}
    products = []
    for row in rows:
        rental = row.get("rentalPrice")
        purchase = row.get("purchasePrice")

        if rental is not None and purchase is not None:
            price_text = f"{rental:,} / {purchase:,}"
        elif rental is not None:
            price_text = f"{rental:,}"
        elif purchase is not None:
            price_text = f"{purchase:,}"
        else:
            price_text = "ー"

        products.append({
            "id": row["id"],
            "name": row["name"],
            "brand": row["brand"] or "",
            "price": price_text,
            "image_path": row["image_path"] or "default.png"
        })

    # ひとつのカテゴリの商品
    categories[category] = products

    return render_template(
        "top/member_index.html",
        categories=categories,
        user_id=user_id,
        single_category=True  # カテゴリモード
    )
    
#性別によるの商品一覧
@top_bp.route('/for/<for_value>', methods=['GET'])
def for_products(for_value):
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None

    con = connect_db()
    cur = con.cursor(dictionary=True)

    sql = """
        SELECT 
            p.id,
            p.name,
            p.rentalPrice,
            p.purchasePrice,
            p.`for`,
            c.name AS category,
            b.name AS brand,
            m.img AS image_path
        FROM m_product AS p
        LEFT JOIN m_brand AS b ON p.brand_id = b.id
        LEFT JOIN m_productimg AS m ON p.id = m.product_id
        LEFT JOIN m_category AS c ON p.category_id = c.id
        WHERE p.`for` = %s
        AND
            p.draft = 0
    """
    cur.execute(sql, (for_value,))
    rows = cur.fetchall()
   
    # TOPページと一緒
    categories = {}
    for row in rows:
        rental = row.get("rentalPrice")
        purchase = row.get("purchasePrice")

        # 価格表示の決定
        if rental is not None and purchase is not None:
            price_text = f"{rental:,} / {purchase:,}"
        elif rental is not None:
            price_text = f"{rental:,}"
        elif purchase is not None:
            price_text = f"{purchase:,}"
        else:
            price_text = "ー"

        # 分類 category
        cat = row["category"] or "その他"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            "id": row["id"],
            "name": row["name"],
            "brand": row["brand"] or "",
            "price": price_text,
            "image_path": row["image_path"] or "default.png"
        })

    cur.close()
    con.close()

    #  member_index.htmlで表示
    return render_template(
        "top/member_index.html",
        categories=categories,
        user_id=user_id,
        selected_for=for_value,
        single_category=True
    )
            
#brandによるの商品一覧
@top_bp.route('/brand/<brand_name>', methods=['GET'])
def brand_products(brand_name):
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None

    con = connect_db()
    cur = con.cursor(dictionary=True)

    sql = """
        SELECT 
            p.id,
            p.name,
            p.name,
            p.rentalPrice,
            p.purchasePrice,
            c.name AS category,
            b.name AS brand,
            m.img AS image_path
        FROM m_product AS p
        LEFT JOIN m_brand AS b ON p.brand_id = b.id
        LEFT JOIN m_productimg AS m ON p.id = m.product_id
        LEFT JOIN m_category AS c ON p.category_id = c.id
        WHERE b.name = %s
        AND
            p.draft = 0
    """
    cur.execute(sql, (brand_name,))
    rows = cur.fetchall()

   
    # TOPページと一緒
    categories = {}
    for row in rows:
        rental = row.get("rentalPrice")
        purchase = row.get("purchasePrice")

        # 価格表示の決定
        if rental is not None and purchase is not None:
            price_text = f"{rental:,} / {purchase:,}"
        elif rental is not None:
            price_text = f"{rental:,}"
        elif purchase is not None:
            price_text = f"{purchase:,}"
        else:
            price_text = "ー"

        # 分類 category
        cat = row["category"] or "その他"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            "id": row["id"],
            "name": row["name"],
            "brand": row["brand"] or "",
            "price": price_text,
            "image_path": row["image_path"] or "default.png"
        })

    cur.close()
    con.close()

    #  member_index.htmlで表示
    return render_template(
        "top/member_index.html",
        categories=categories,
        user_id=user_id,
        selected_brand=brand_name
    )
    
# subkariについての表示
@top_bp.route('/about_subkari', methods=['GET'])
def about_subkari():
    if 'user_id' in session:
        user_id = session.get('user_id')
    else :
        user_id = None
    
    resp = make_response(render_template('top/welcome_subkari.html', user_id = user_id))
    return resp

# 商品についての表示 (トップス)
@top_bp.route('/tops', methods=['GET'])
def tops():
    # =======================================================================
    #  修正点: DUMMY_PRODUCTSをテンプレートに渡すように変更
    # search_query も None で渡すことで全商品一覧として表示
    # =======================================================================
    context = {
        'search_query': None,
        'products': DUMMY_PRODUCTS # 50件のダミー商品を渡す
    }
    return render_template('top/search_product.html', **context)

# 商品についての表示 (ボトムス)
@top_bp.route('/bottoms', methods=['GET'])
def bottoms():
    # 商品の検索処理やデータベースのクエリを追加する
    # ダミーデータを渡す場合は上記 tops() と同様の処理が必要です
    return render_template('top/search_product.html', search_query=None, products=DUMMY_PRODUCTS)

# 商品についての表示 (アクセサリー)
@top_bp.route('/accessories', methods=['GET'])
def accessories():
    # DUMMY_PRODUCTSから全ての商品を渡す（フィルタリングなし）
    return render_template('top/search_product.html', search_query=None, products=DUMMY_PRODUCTS)

# コーディネート
@top_bp.route('/coordinate', methods=['GET'])
def coordinate():
    # DUMMY_PRODUCTSから全ての商品を渡す（フィルタリングなし）
    return render_template('top/search_product.html', search_query=None, products=DUMMY_PRODUCTS)


# 検索結果についての表示#########################################################################################################################################
@top_bp.route('/search', methods=['GET'])
def search():
     # user検証成功
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    #Get the Keyword and Page
    search_query = request.args.get('keyword', '').strip()
    page = int(request.args.get('page', 1))
    
    #Limit of the showed products on page
    limit = 5
    offset = (page - 1) * limit
    
    #件数計算のsql
    sql_count = """
        SELECT COUNT(*) AS count
        FROM m_product AS p
        LEFT JOIN m_brand AS b
        ON p.brand_id = b.id
        LEFT JOIN m_productimg AS i
        ON p.id = i.product_id
        WHERE (%s = '' OR p.name LIKE %s)
        AND
            p.draft = 0
    """
    params_count = [search_query, f"%{search_query}%"]
    #sql実行
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql_count, params_count)
    result = cur.fetchone()
    if result is None:
        total_count = 0
    else:        
        total_count = int(result['count'])
    cur.close()
    con.close()
    #page数
    total_pages = math.ceil(total_count / limit)

    #商品資料のsql
    sql_select = """
        SELECT 
            p.*,
            b.name AS brand_name,
            i.img
        FROM m_product AS p
        LEFT JOIN m_brand AS b ON p.brand_id = b.id
        LEFT JOIN m_productimg AS i ON p.id = i.product_id
        WHERE (%s = '' OR p.name LIKE %s)
        AND
            p.draft = 0
        GROUP BY p.id
        ORDER BY p.id DESC
        LIMIT %s OFFSET %s
    """
    params_select = [search_query, f"%{search_query}%", limit, offset]
    #sql実行
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql_select, params_select)
    products = cur.fetchall()
    cur.close()
    con.close()

    #価格のレンタル/購買処理
    for p in products:
        rental = p.get("rentalPrice")
        purchase = p.get("purchasePrice")
        if rental is not None and purchase is not None:
            p["price"] = f"{rental:,} / {purchase:,}"
        elif rental is not None:
            p["price"] = rental
        elif purchase is not None:
            p["price"] = purchase
        else:
            p["price"] = 0

    return render_template(
        "top/search_product.html",
        search_query=search_query,
        products=products,
        total_pages=total_pages,
        current_page=page,
        user_id = user_id
        )    


# 商品詳細についての表示
@top_bp.route('/product_details', methods=['GET'])
def product_details():
    if 'user_id' in session:
        user_id = session.get('user_id')
    else:
        user_id = None

    # 'top/search_product.html' テンプレートをレンダリング
    resp = make_response(render_template('products/search_product.html', user_id=user_id))
    return resp

# DB設定 (使用しないが元のコードに残す)
def connect_db():
    con=mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = '',
        db ='db_subkari'
    )
    return con
