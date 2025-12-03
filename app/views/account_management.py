# from flask import Flask
# from flask import render_template,Blueprint
# import mysql.connector


# #DB設定------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def connect_db():
#     con=mysql.connector.connect(
#         host = 'localhost',
#         user = 'root',
#         passwd = '',
#         db ='db_subkari'
#     )
#     return con


# account_management_bp = Blueprint('account_management',__name__,url_prefix='/account_management')





# #アカウント管理ページ ------------------------------------------------
# @account_management_bp.route("/account_management")
# def account_management():
#     sql='''
#     select 
#     a.id,
#     a.username as アカウント名,
#     a.status as 状況,
#     a.created_at as 作成日時,
#     max(l.logoutDatetime) as 最終ログイン時刻

#     from m_account a
#     inner join t_login l on a.id=l.account_id

#     group by a.id , a.username , a.status , a.created_at 
#     order by a.id
#     ; 
#     '''
#     con=connect_db()
#     cur=con.cursor(dictionary=False)

#     #アカウントの簡易表示情報取得 
#     cur.execute(sql)   #今のままだと全件表示するようになってるから、何件表示するか検討の余地あり
#     cur.close()
#     user_list=cur.fetchall()
#     return render_template("account_management.html",user_list=user_list)

