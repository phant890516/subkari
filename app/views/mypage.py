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

#価格をカンマ区切りにして返す ----------------------------------------------------
def comma(num):
    #0が来た場合の処理
    if num==0:
        return str(num)
    
    string1=""
    string2=""
    if type(num)=="string":
        num=int(num)
    tmp=num
   
    count=0
 
    while tmp/10!=0:
        string1+=str(tmp%10)
        tmp//=10
        count+=1
        if count%3==0 :
            string1+=","
            count+=1
    tmp=0
    while tmp<count:
        string2+=string1[count-tmp-1]
        tmp+=1

    return string2
    

#アカウントの口座情報を取得する ------------------------------------------------------------------------------
def getAccountInfo():
    accountNumbers=[]                 #口座番号下位三桁を格納
    id=session["user_id"]
    editmode=session["editmode"]
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
    return bank_info,accountNumbers,count

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

#mypageこういう名前のモジュール
mypage_bp = Blueprint('mypage', __name__, url_prefix='/mypage')


# ---------------------------------------------------------------------------------------------



#マイページトップ表示-----------------------------------------------------------------------------
@mypage_bp.route("/mypage")
def mypage():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    
    
    #アカウントテーブルからユーザー情報を取得
    user_info=get_user_info(user_id)
    evaluation,evaluationCount,follows,followers,products=get_transaction_info(user_id)

    con=connect_db()
    cur=con.cursor(dictionary=True)
    
    #売上履歴を取得
    #売上履歴から売上金を計算する
    sql="select p.id ,ti.created_at, case when t.situation='購入' then p.purchasePrice else p.rentalPrice end as price from t_transaction t inner join m_product  p on t.product_id=p.id left join t_time ti on t.id=ti.transaction_id where t.status='取引完了' and p.account_id=%s group by ti.created_at,t.seller_id"
    cur.execute(sql,(user_id,))
    sales=cur.fetchall()
    total=0
    for sale in sales:
        total+=int(sale['price'] if sale['price'] else 0)
    total=comma(total)

    return render_template("mypage/mypage.html",
    evaluation=evaluation,evaluationCount=evaluationCount,follows=follows,
    followers=followers,products=products,user_info=user_info ,user_id=user_id,total=total)
    
#------------------------------------------------------------------------------------------------


#editProfile プロフィール編集ページ表示--------------------------------------------------------------
@mypage_bp.route("/editProfile")
def editProfile():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    #user情報を取得
    user_info=get_user_info(user_id)
    evaluation,evaluationCount,follows,followers,products=get_transaction_info(user_id)
    #商品情報を取得
    productId,productName,productImg=get_product_info(user_id)
    print(productId)
    return render_template("mypage/editProfile.html",evaluation=evaluation,evaluationCount=evaluationCount,follows=follows,followers=followers,products=products,productId=productId,productName=productName,productImg=productImg,user_info=user_info,user_id=user_id)

#updateProfile プロフィール更新--------------------------------------------------------------
@mypage_bp.route("/updateProfile",methods=['POST'])
def updateProfile():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    #更新内容を取得
    new_profile=request.form   #username,smoker,introduction

    id=session['user_id']

    #dbに更新をかける 
    con = connect_db()
    cur = con.cursor(dictionary=True)
    sql="update m_account set username=%s,smoker=%s,introduction=%s where id=%s"
    cur.execute(sql,(new_profile['username'],new_profile['smoker'],new_profile['introduction'],id))
    con.commit()
    cur.close()
    con.close()

    #更新後のユーザー情報を取得 
    user_info=get_user_info(id)
    evaluation,evaluationCount,follows,followers,products=get_transaction_info(id)
    productName,productImg=get_product_info(id)
    return render_template("mypage/editProfile.html",user_info=user_info,evaluation=evaluation,evaluationCount=evaluationCount,follows=follows,followers=followers,products=products,productName=productName,productImg=productImg,user_id=user_id)

    
#--------------------------------------------------------------------------------------------------

#edit プロフィール編集-------------------------------------------------------------------------------
@mypage_bp.route("/edit")
def edit():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    #ユーザー情報を取得
    user_info=get_user_info(user_id)

    return render_template("mypage/edit.html", user_info=user_info,user_id=user_id)
    

#--------------------------------------------------------------------------------------------------


#bankRegistration　振込口座登録ページ表示--------------------------------------------------------------
@mypage_bp.route("/bankRegistration")
def bankRegistration():

    #登録されている口座数を取得
    bank_count=0
    id=session["user_id"]
    con=connect_db()
    cur=con.cursor(dictionary=True)

    sql="select count(*) as 登録数 from t_transfer t inner join m_account a on t.account_id=a.id where a.id=%s group by a.id"
    cur.execute(sql,(id,))
    
    bank_count=cur.fetchone()
    if bank_count==None:
        bank_count=0
    else:
        bank_count=int(bank_count["登録数"])
    
    
    cur.close()
    con.close()
    #3件すでに登録済みなら拒否する
    if bank_count>=3:
    #     return render_template("mypage/mypage.html",user_id=user_id)
    
    # return render_template("mypage/bankRegistration.html",user_id=user_id)
        return render_template("mypage/mypage.html")
    
    return render_template("mypage/bankRegistration.html")
#----------------------------------------------------------------------------------------------------

#bankComplete' 振込口座登録完了ページ------------------------------------------------------------------
@mypage_bp.route("/bankComplete",methods=['POST'])
def bankComplete():
    #エラーチェック
    #error回数とメッセージ
    ecnt = 0
    error_message={}
    bank_info=request.form    #name,accountType,branchCode,accountNumber,firstName,famillyName
    #空欄確認
    for key,value in bank_info.items():
        if not value:
            ecnt+=1
    #空欄あり、登録できない      
    if ecnt !=0:
        return render_template('mypage/bankRegistration.html')
        # return render_template('mypage/bankRegistration.html',user_id=user_id)
    
    #既に登録されていないか調べる 
    id=session["user_id"]
    sql="select * from t_transfer  where (account_id=%s) and (branchCode=%s) and (accountNumber=%s)"
    con=connect_db()
    cur=con.cursor(dictionary=True)
    cur.execute(sql,(id,bank_info['branchCode'],bank_info['accountNumber']))
    bankSame=cur.fetchone()

    #登録されているのでエラー
    if bankSame is not None:
        return render_template('mypage/bankRegistration.html')
        # return render_template('mypage/bankRegistration.html',user_id=user_id)
    
    accountHolder=bank_info['famillyName']+bank_info['firstName']
    #登録処理

    #データを追加
    sql="INSERT INTO t_transfer (account_id,bankName,accountType,branchCode,accountNumber,accountHolder) VALUES(%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (id,bank_info['name'],bank_info['accountType'],bank_info['branchCode'],bank_info['accountNumber'],accountHolder))          #アカウントidがわからない
    con.commit()
    cur.close()
    return render_template("mypage/bankComplete.html")
    # return render_template("mypage/bankComplete.html",user_id=user_id)
#----------------------------------------------------------------------------------------------------

#bank_transfer 振込申請ページ表示---------------------------------------------------------------------
@mypage_bp.route("mypage/transferApplication")
def transferApplication():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    session["editmode"]=False
    bank_info,accountNumbers,count=getAccountInfo()
    editmode=session["editmode"]
    return render_template("mypage/transferApplication.html",user_id=user_id,bank_info=bank_info,accountNumbers=accountNumbers,count=count,editmode=editmode)
#---------------------------------------------------------------------------------------------------
#transferApplication 削除ボタン表示 -----------------------------------------------------------------
@mypage_bp.route("/transferApplication")
def editActivate():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    editmode=session["editmode"]
    if not editmode:
        session["editmode"]=True
    else:
        session["editmode"]=False
    editmode=session["editmode"]
    bank_info,accountNumbers,count=getAccountInfo()
   
    
    return render_template("mypage/transferApplication.html",user_id=user_id,bank_info=bank_info,accountNumbers=accountNumbers,count=count,editmode=editmode)

#transferApplication 登録口座削除 -------------------------------------------------------------------
@mypage_bp.route("/transferApplication/removeBank",methods=['POST'])
def removeBank():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    #何番目が選択されたかを取得
    bank_id = request.form.get("bank_id") 

    id=session["user_id"]
    sql="select * from t_transfer  where account_id=%s"
    con=connect_db()
    cur=con.cursor(dictionary=True)
    cur.execute(sql,(id,))
    target=cur.fetchall()
    #選択された口座のidを取得
    target_id=target[int(bank_id)]["id"]

    #削除
    sql="delete from t_transfer where id=%s"
    cur.execute(sql,(target_id,))
    con.commit()
    cur.close()
    con.close()
    bank_info,accountNumbers,count=getAccountInfo()
    editmode=session["editmode"]
    
    return render_template("mypage/transferApplication.html",user_id=user_id,bank_info=bank_info,accountNumbers=accountNumbers,count=count,editmode=editmode)


#transferAmount 金額選択ページ表示--------------------------------------------------------------------
@mypage_bp.route("/transferAmount", methods=["GET", "POST"])
def transferAmount():
    error_message = None

    if request.method == "POST":
        amount_str = request.form.get("amount")

        if not amount_str:
            error_message = "金額を入力してください。"
        else:
            try:
                amount = int(amount_str)
                if amount < 0:
                    error_message = "金額は0円以上を入力してください。"
                elif amount > 1000000:
                    error_message = "一度に振り込める限度額は1,000,000円までです。"
                elif amount < 201:
                    error_message = "振込手数料200円を含め、最低201円以上を入力してください。"
            except ValueError:
                error_message = "正しい金額を入力してください。"

        if error_message:
            # 入力エラーがあれば同じページにエラーメッセージ付きで再表示
            return render_template("mypage/transferAmount.html", error_message=error_message)

        # ✅ 正常処理時はマイページ完了画面へリダイレクト
        return redirect(url_for('mypage.amountComp'))

    # ✅ GETアクセス時（初回表示）
    return render_template("mypage/transferAmount.html")


#---------------------------------------------------------------------------------------------------


#金額確定ページ------------------------------------------------------------------------------------
@mypage_bp.route("/mypage/amountComp")
def amountComp():
    return render_template("mypage/amountComp.html")
#---------------------------------------------------------------------------------------------------

#レンタルと購入で値段の区別がつかないため支払った額がわからない
#salesHistory 売上履歴------------------------------------------------------------------------------
@mypage_bp.route("/salesHistory")
def salesHistory():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    datetimes=[]
    prices=[]
    ids=[]
    con=connect_db()
    cur=con.cursor(dictionary=True)
    
    #売上履歴を取得
    #売上履歴は取引テーブルでステータスが取引完了のものを取得
    sql="select p.id ,ti.created_at, case when t.situation='購入' then p.purchasePrice else p.rentalPrice end as price from t_transaction t inner join m_product  p on t.product_id=p.id left join t_time ti on t.id=ti.transaction_id where t.status='取引完了' and p.account_id=%s group by ti.created_at,t.seller_id"
    cur.execute(sql,(user_id,))
    #id,created_at,price
    salesHistory=cur.fetchall()
    
    for history  in salesHistory:
        datetimes.append(history['created_at'])
        #価格をカンマ区切りにしてから配列に格納
        prices.append(comma(history['price']))
        ids.append(history['id'])

    cur.close()
    con.close()
    return render_template("mypage/salesHistory.html" ,  user_id=user_id,datetimes=datetimes,prices=prices,ids=ids)
#-------------------------------------------------------------------------------------------------



#振込履歴-----------------------------------------------------------------------------------------
@mypage_bp.route("/transferHistory")
def transferHistory():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    con=connect_db()
    cur=con.cursor(dictionary=True)
    sql="select  from t_transaction t inner join m_product p on t.product_id=p.id where t.seller_id=%s and t.status='取引完了'"

    #売上履歴を取得
    #売上履歴は取引テーブルでステータスが取引完了のものを取得
    return render_template("mypage/transferHistory.html" ,  user_id=user_id)
#------------------------------------------------------------------------------------------------

#todo.html やることリスト-------------------------------------------------------------------------
@mypage_bp.route("/todo")
def todo():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')


    # con=connect_db()
    # cur=con.cursor(dictionary=True)
    # sql="select bankName,accountNumber,branchCode from t_transfer  where account_id=%s limit 3"
    # cur.execute(sql,(id,))
    # todo=cur.fetchall()
    # cur.close()
    # con.close()


    return render_template("mypage/todo.html" ,  user_id=user_id )
#------------------------------------------------------------------------------------------------
@mypage_bp.route('/personal_info')
def personal_info():
    # 個人情報編集ページの処理
    return render_template('mypage/personal_info.html')


#privacy_policy プライバシーポリシー表示---------------------------------------------------------------
@mypage_bp.route("/privacyPolicy")
def privacyPolicy():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    con=connect_db()
    cur=con.cursor(dictionary=True)
    sql="select content_detail from m_admin_contents  where id=2"
    cur.execute(sql)
    result=cur.fetchone()
    cur.close()
    con.close()
    

    return render_template("mypage/privacyPolicy.html" ,  user_id=user_id , result=result)
#--------------------------------------------------------------------------------------------------------------------

#terms 利用規約表示  ----------------------------------------------------------------------------------------
@mypage_bp.route("/terms")
def terms():
    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    con=connect_db()
    cur=con.cursor(dictionary=True)
    sql="select content_detail from m_admin_contents  where id=1"
    cur.execute(sql)
    result=cur.fetchone()
    cur.close()
    con.close()
    

    return render_template("mypage/terms.html" ,  user_id=user_id , result=result)
#--------------------------------------------------------------------------------------------------------------------

# helpCenter ヘルプセンター表示ページ
@mypage_bp.route("/helpCenter")
def helpCenter():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')
    
    return render_template("mypage/helpCenter.html", user_id=user_id)


#問い合わせ----------------------------------------------------------------------------------------------------------
@mypage_bp.route("/inquiry")
def inquiry():

    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    return render_template("mypage/inquiry.html" , user_id=user_id  )
#-------------------------------------------------------------------------------------------------------------------
    
#いいね一覧---------------------------------------------------------------------------------------------------------
@mypage_bp.route("/likes")
def likes():

    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')


    con=connect_db()
    cur=con.cursor(dictionary=True)
    sql = """
    SELECT 
        p.id, 
        p.name, 
        p.purchasePrice, 
        p.rentalPrice, 
        p.purchaseFlg, 
        p.rentalFlg, 
        MIN(i.img) AS image_path
    FROM t_favorite f
    JOIN m_product p ON f.product_id = p.id
    LEFT JOIN m_productimg i ON p.id = i.product_id
    WHERE f.account_id = %s
    GROUP BY p.id, p.name, p.purchasePrice, p.rentalPrice, p.purchaseFlg, p.rentalFlg;
"""

    cur.execute(sql, (user_id,))
    likes_list = cur.fetchall()

    cur.close()
    con.close()  
    # print(likes_list)


    return render_template("mypage/likes.html" ,  user_id=user_id , likes_list=likes_list)
#------------------------------------------------------------------------------------------------------------------

#フォローリスト ---------------------------------------------------------------------------------------------------------
@mypage_bp.route("/follow")
def follow():

    if 'user_id' not in session:
        user_id = None
        return redirect(url_for('login.login'))
    else:
        user_id = session.get('user_id')

    follow_list=[]
    con=connect_db()
    cur=con.cursor(dictionary=True)

    #フォローしているアカウントのid、アカウント名、評価、評価件数を取得
    sql='''
    SELECT 
        a.id as id, a.username as ユーザー名,a.profileImage as アイコン,
        (
            SELECT AVG(e.score)
            FROM t_evaluation e
            WHERE e.recipient_id = a.id
        ) AS 評価,
        (
            SELECT count(e.score)
            FROM t_evaluation e
            WHERE e.recipient_id = a.id
        ) as 評価件数
    FROM m_account a
    WHERE a.id IN (
        SELECT target_id
        FROM t_connection 
        WHERE type='フォロー'
        AND execution_id=%s
    );
        '''
    cur.execute(sql,(user_id,))
    follow_list=cur.fetchall()
    #評価を整数値に変換
    for f in follow_list:
        if f['評価'] is not None:
            f['評価']=int(f['評価'])
        else:
            f['評価']=0   # 評価が無い人は0
            f['評価件数']=0

    cur.close()
    con.close()
    return render_template("mypage/followList.html",follow_list=follow_list,user_id=user_id)

