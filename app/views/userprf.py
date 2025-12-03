from flask import Blueprint , render_template ,request,make_response,redirect,url_for,session
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime , timedelta
import mysql.connector
import json
import os

#DB設定------------------------------------------------------------------------------------------------------------------------------------------------------------------
def connect_db():
    con=mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = '',
        db ='db_subkari'
    )
    return con
#------------------------------------------------------------------------------------------------------------------------------------------------------
#ユーザー情報を取得する ------------------------------------------------------------------------------------
#引数として受け取ったidを持つユーザーの情報を取得
def get_user_info(id):
    sql = "SELECT * FROM m_account WHERE id = %s"
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql, (id,))  # ← タプルで渡す！
    user_info = cur.fetchone()
    return user_info


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

    if followers is None:
        followers={'フォロワー数':0}
    if follows is None:
        follows={'フォロー数':0}
    if products is None:
        products={'出品数':0}
    


    if evaluation is not None:


        evaluation['評価'] = round(float(evaluation['評価']))
    #小数点型にしてから四捨五入
    else:
        evaluation = {"評価":0}
        



    return evaluation,evaluationCount,follows,followers,products

#商品データを取得 --------------------------------------------------
def get_product_info(id):

    con = connect_db()
    cur = con.cursor(dictionary=True)

    #商品idを取得
    sql="select id from m_product where account_id=%s"
    cur.execute(sql,(id,))
    product_id=cur.fetchall()
    #商品名を取得
    sql="select name from m_product where account_id=%s"
    cur.execute(sql,(id,))
    name=cur.fetchall()
    #各商品1枚目の画像を取得 
    sql="SELECT  i.* FROM m_productImg i INNER JOIN (SELECT  product_id,MIN(id) AS first_image_id FROM m_productImg GROUP BY product_id) AS first_img ON i.id = first_img.first_image_id INNER JOIN m_product p ON p.id = i.product_id WHERE p.account_id = %s"
    cur.execute(sql,(id,))
    img=cur.fetchall()
    cur.close()
    con.close()

    return product_id,name,img


# Blueprintの設定
userprf_bp = Blueprint('userprf', __name__, url_prefix='/userprf')


#userprf ユーザープロフィールを表示------------------------------------------------------
# @userprf_bp.route("/<int:userprf_id>" )
@userprf_bp.route("/userprf" ,methods=["POST","GET"])
def userprf():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    id=request.form.get("id")
    
    #user情報を取得
    user_info=get_user_info(id)
    evaluation,evaluationCount,follows,followers,products=get_transaction_info(id)
    #商品情報を取得
    productId,productName,productImg=get_product_info(id)
 
  
    return render_template("userprf/userprf.html",evaluation=evaluation,evaluationCount=evaluationCount,follows=follows,followers=followers,products=products,productId=productId,productName=productName,productImg=productImg,user_info=user_info,user_id=user_id)


#--------------------------------------------------------------------------------------