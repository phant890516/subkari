from flask import Blueprint , render_template ,request,make_response,redirect,url_for,session
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime , timedelta
import mysql.connector
import json
import os

login_bp = Blueprint('login', __name__, url_prefix='/login')



# ----------------------------------------------------------------------
# 設定
# ----------------------------------------------------------------------
# 保存先: SUBKARI/app/static/img/IdentityImg/
UPLOADS_RELATIVE_PATH = 'app/static/img/IdentityImg'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """許可された拡張子かどうかをチェックするヘルパー関数"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#登録完了画面表示----------------------------------------------------------------------------------------------------------------------------------------------------------
# 登録完了画面表示
@login_bp.route('/registration_complete', methods=['GET'])
def registration_complete():
    # 登録完了画面で表示するメッセージなどを渡す場合
    message = "ユーザー登録が完了しました。"
    return render_template('login/registration_complete.html', message=message)

#Login画面表示----------------------------------------------------------------------------------------------------------------------------------------------------------
@login_bp.route('/login',methods=['GET'])
def login():
    #errorメッセージ
    etbl={}
    account={}
    return render_template('login/login.html',etbl=etbl,account=account)

#Login確認--------------------------------------------------------------------------------------------------------------------------------------------------------------
@login_bp.route('/login/auth',methods=['POST'])
def login_auth():
    #mail,password取得
    account = request.form
    
    #error回数とメッセージ
    ecnt = 0
    error_message={}
    
    #空欄確認
    for key,value in account.items():
        if not value:
            ecnt+=1
    #空欄あり、登録できない      
    if ecnt !=0:
        return render_template('login/login.html',account=account)
    
    # 入力した資料がデータベースに存在するかどうかを確認
    sql = "SELECT * FROM m_account WHERE mail = %s;"
    con=connect_db()
    cur=con.cursor(dictionary=True)
    cur.execute(sql,(account['mail'],))
    # ここで確認
    userExist = cur.fetchone()
    #ユーザーが存在しないまたはパスワードが一致しない
    if not userExist or userExist['password'] != account['password']:
        error_message = "メールアドレスまたはパスワードが正しくありません。"
        return render_template('login/login.html',account=account,error_message = error_message)
    
    #登録成功の処理
    session['user_id'] = userExist['id']

    return redirect(url_for('top.member_index'))
    
#Logout--------------------------------------------------------------------------------------------------------------------------------------------------------------
@login_bp.route('/login/logout',methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('top.guest_index'))

#Register-------------------------------------------------------------------------------------------------------------------------------------------------------------
# @login_bp.route("/register_user", methods=["GET"])
# def show_register_user():
#     account = {}
#     result = {"content_detail": ""}
#     return render_template("login/new_account.html", account=account, result=result)

@login_bp.route("/register_user", methods=["GET"])
def show_register_user():
    account = {}
    
    # 利用規約を DB から取得
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT content_detail FROM m_admin_contents WHERE id=1")
    result = cur.fetchone()
    cur.close()
    con.close()
    
    # DB にデータがない場合の安全策
    if not result:
        result = {"content_detail": "利用規約の内容が登録されていません。"}
    
    return render_template("login/new_account.html", account=account, result=result)
@login_bp.route("/terms", methods=["GET"])
def show_terms():
    # DBから利用規約を取得
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT content_detail FROM terms WHERE id = 1")
    result = cur.fetchone()
    cur.close()
    con.close()
    if not result:
        result = {"content_detail": ""}
    return render_template("mypage/terms.html", result=result)


#プライバシーポリシー表示---------------------------------------------------------------------------------------------------------------------------------------------------------- 
@login_bp.route('/privacy_policy',methods=['GET'])
def privacy_policy():
    return render_template('login/privacy.html')


#Register確認----------------------------------------------------------------------------------------------------------------------------------------------------------
@login_bp.route('/register_user/complete',methods=['POST'])
def register_user_complete():
    account = request.form
    error = ""
    error_same = ""
    # 入力確認
    if account['password'] != account['password_confirm']:
        error = "メールアドレスまたはパスワードが正しくありません。"
        return render_template('login/new_account.html', error=error, account=account)
    
    
    #同一user確認    
    # con = None  # データベース接続オブジェクトを初期化
    # cur = None  # カーソルオブジェクトを初期化
    

    # 参考コードをここに応用します
    sql = "SELECT * FROM m_account WHERE mail = %s;"
    
    # connect_db() はご自身の環境で定義されているDB接続関数と想定しています
    con = connect_db() 
    cur = con.cursor(dictionary=True)
    
    # フォームから受け取ったメールアドレスをプレースホルダ(%s)に渡します
    # (account['mail'],) のようにカンマを付けてタプルにすることが重要です
    cur.execute(sql, (account['mail'],)) 
    
    # fetchone() で結果を1件取得します
    userExist = cur.fetchone()
    
    # existing_user が None でない場合 ＝ データが取得できた ＝ 既に使用されている
    if userExist:
        error_same = "メールアドレスまたはパスワードが正しくありません。"
        # エラーなので、テンプレートをレンダリングして処理を終了します

        cur.close()
        con.close()
        return render_template('login/new_account.html', error=error, error_same=error_same)

    #ここからセッション登録して次の画面にせんいする
    # account の中身（イメージ）
    # {
    #   'mail': 'test@example.com',
    #   'password': 'password123',
    #   'password_confirm': 'password123'
    # }

    # データをセッションに登録
    # request.form (ImmutableMultiDict) を通常の辞書 (dict) に変換して保存
    session_data = dict(account)
    # セッションに 'registration_data' というキーで保存
    #このキーをつくってログイン状態のセッションと区別する(user_id)。
    # session オブジェクト全体の中身（イメージ）
    # {
    #   'registration_data': {
    #     'mail': 'test@example.com',
    #     'password': 'password123',
    #     'password_confirm': 'password123'
    #   }
    session['registration_data'] = session_data

    # ◆ 処理が正常終了した場合もDB接続をクローズします
    cur.close()
    con.close()
    
    return redirect(url_for('login.show_register_form'))



    #DBに登録
    # user = (account['mail'],account['password'])
    # sql = "INSERT INTO m_account (mail,password) VALUES(%s,%s)"
    # cur.execute(sql,user)  
    # con.commit()
    # cur.close()
    # con.close()



# @login_bp.route("/register_user_complete", methods=["POST"])
# def handle_register_user_complete():
#     mail = request.form.get("mail")
#     password = request.form.get("password")
#     password_confirm = request.form.get("password_confirm")

#     if password != password_confirm:
#         error = "パスワードが一致しません。"
#         return render_template("register_user.html", error=error, account={"mail": mail})

#     session["user"] = {
#         "mail": mail,
#         "password": password
#     }

#     return redirect(url_for("login.register_complete"))


    # return redirect(url_for('top.new_account',account_id = account["mail"]))


#登録フォーム表示
@login_bp.route("/register_user/form", methods=["GET"])
def show_register_form():
    """
    住所・電話番号フォーム（register_form.html）を表示する
    前のステップ（メール・パスワード登録）が完了しているかセッションをチェックする
    """
    # セッションに 'registration_data' がなければ、無効なアクセスとみなし最初のフォームへリダイレクト
    if 'registration_data' not in session:
        # show_register_user は最初のフォーム（new_account.html）を表示するルート名
        return redirect(url_for('login.show_register_user')) 
        
    # セッションデータがあれば、フォームを表示する
    # 初回表示のため、エラーとフォームデータは空で渡す
    return render_template(
        'login/register_form.html', 
        errors={}, 
        form_data={}
    )



# DBスキーマに対応するバリデーションルール
# m_address テーブルの定義に基づき設定

# Flaskのルート関数（registration_form_complete）の「前」に、
# この辞書を定義します。

# 'name属性': (最大文字数, 必須か否か) のタプル
# 最大文字数: SQLのVARCHAR(N)やCHAR(N)のNの値。
#             DATE, INT, BOOLEAN型は文字列長ではないため「None」とします。
# 必須か否か: SQLで「NOT NULL」が指定されていれば「True」。
#             「NULL」許容（指定なし）であれば「False」。

ACCOUNT_SCHEMA = {
    # --- m_account ---------------------------------------------
    # 1. アカウント名
    'username':          (12, True),   # m_account.username VARCHAR(12) NOT NULL
    
    # 2. 姓 (全角)
    'lastName':        (50, True),   # m_account.lastName VARCHAR(50) NOT NULL
    
    # 3. 名 (全角)
    'firstName':       (50, True),   # m_account.firstName VARCHAR(50) NOT NULL
    
    # 4. セイ (全角)
    'lastNameKana':   (50, True),   # m_account.lastNameKana VARCHAR(50) NOT NULL
    
    # 5. メイ (全角)
    'firstNameKana':  (50, True),   # m_account.firstNameKana VARCHAR(50) NOT NULL
    
    # 6. 生年月日
    'birthday':         (None, True), # m_account.birthday DATE NOT NULL
    
    # --- m_address ---------------------------------------------
    # 7. 郵便番号
    'zip':              (7, True),    # m_address.zip CHAR(7) NOT NULL
    
    # 8. 都道府県
    'pref':             (10, True),   # m_address.pref VARCHAR(10) NOT NULL
    
    # 9. 市区町村
    'address1':         (20, True),   # m_address.address1 VARCHAR(20) NOT NULL
    
    # 10. 番地
    'address2':         (20, True),   # m_address.address2 VARCHAR(20) NOT NULL
    
    # 11. 建物名
    'address3':         (40, False),  # m_address.address3 VARCHAR(40) NULL
    
    # --- m_account (続き) --------------------------------------
    # 12. 電話番号
    'tel':              (20, True),   # m_account.tel VARCHAR(20) NOT NULL
                                      # (HTMLのmaxlength(11)よりDBが大きいので安全)
    # 13. 喫煙の有無
    'smoker':           (None, True), # m_account.smoker boolean NOT NULL
}

#入力フォーム確認-電話番号や住所
@login_bp.route("register_user/form_complete", methods=["POST"])
def registration_form_complete():

    # session['registration_data'] = None


    # セッションにデータがなければ、フォームに戻す
    if 'registration_data' not in session:
        return redirect(url_for('login.show_register_user'))
    
    # 1. フォームからデータを取得
    form_data = request.form
    errors = {} # エラーメッセージを格納する辞書


    #文字数チェック
    #ADDRESS_SCHEMAに入っているmax_lengthを参考に比較する。
    
    # 2. バリデーションループ
    for name, (max_length, is_required) in ACCOUNT_SCHEMA.items():
        value = form_data.get(name)
        
        # --- 必須チェック ---
        if is_required and not value:
            # 「建物名」のように必須(False)でない項目は、
            # 未入力でもこのエラーを通過します。
            
            # (特殊ケース) 「喫煙の有無」は
            # HTMLで 'yes' が default checked なので、
            # 'smoker' が未入力になることは通常ありません。
            
            errors[name] = "この項目は必須です。"
            continue # 必須エラーなら文字数チェックはスキップ
            
        # --- 文字数チェック (値が入力されている場合のみ) ---
        if value:
            # max_length が None (DATE型など) の場合はチェックをスキップ
            if max_length is not None:
                if len(value) > max_length:
                    errors[name] = f"{max_length}文字以内で入力してください。"
    
    # (オプション) その他のカスタムバリデーション
    # (例：電話番号が本当に数字か？など)
    tel_value = form_data.get('tel')
    if tel_value and not tel_value.isdigit():
        errors['tel'] = "電話番号はハイフンなしの半角数字で入力してください。"


    # 3. バリデーション結果の確認
    if errors:
        # エラーがある場合：
        # フォームのページをエラーメッセージと共に「再表示」する
        # ※HTML側で errors[name] を表示する処理をする
        
        # register_form.html を再描画
        return render_template(
            'login/register_form.html', 
            errors=errors, 
            form_data=form_data # 入力値をフォームに復元するために渡す
        )
    
    # 4. バリデーション成功時
    else:
        # セッションにデータを保存する
        # (dict()で、不変なMultiDictから変更可能な通常の辞書に変換)

        #既存のセッションデータを取得する(mail.passwordなど)
        existing_data = session.get('registration_data', {})

        #現在のフォームデータ (住所など) を取得
        new_form_data = dict(form_data)

        session['registration_data'] = dict(form_data)

        #二つの辞書を結合し、新しいデータで古いデータを更新/追加する
        existing_data.update(new_form_data)

        #結合したデータをセッションに再格納
        session['registration_data'] = existing_data

        
        # PRGパターン: 次のページ（電話番号認証）にリダイレクトする
        return redirect(url_for('login.show_phone_verification'))

    # return render_template('login/Phone_verification.html')

# 電話番号認証ページ（GET）
@login_bp.route("/phone_verification", methods=["GET"])
def show_phone_verification():
    if 'registration_data' not in session:
        # flash("セッションが切れました。もう一度入力してください。")
        return redirect(url_for('login.show_register_user')) # ★登録フォームのGETルート
        
    return render_template('login/Phone_verification.html')


#SMS確認
@login_bp.route("register_user/phone_auth", methods=["POST"])
def phone_auth():

    # セッション確認
    if 'registration_data' not in session:
        return redirect(url_for('login.show_register_user')) # ★登録フォームのGETルート

    return render_template('login/identity_verification.html')


#SMS再送
@login_bp.route("register_user/phone_auth_resend", methods=["POST"])
def phone_auth_resend():

    # セッション確認
    if 'registration_data' not in session:
        return redirect(url_for('login.show_register_user')) # ★登録フォームのGETルート

    return render_template('login/Phone_verification.html')

#本人確認-登録完了
@login_bp.route("register_user/verification", methods=["POST"])
def verification():
    # セッション確認
    if 'registration_data' not in session:
        return redirect(url_for('login.show_register_user')) # ★登録フォームのGETルート
        

    front_image = request.files.get('front_image')
    back_image = request.files.get('back_image')

    if not front_image or front_image.filename == '':
        message = "本人確認書類の表面画像をアップロードしてください。"
        return render_template('login/identity_verification.html', message=message)
    if not back_image or back_image.filename == '':
        message = "本人確認書類の裏面画像をアップロードしてください。"
        return render_template('login/identity_verification.html', message=message)


    #セッションに入っているデータをdbに登録する。

    # セッションから全登録データを取得
    all_data = session['registration_data']


    # m_account 用のデータ
    account_data = (
        all_data.get('mail'),
        all_data.get('password'), 
        all_data.get('username'),
        all_data.get('lastName'),
        all_data.get('firstName'),
        all_data.get('lastNameKana'),
        all_data.get('firstNameKana'),
        all_data.get('birthday'),
        all_data.get('tel'),
        all_data.get('smoker') == 'yes', # 'yes'/'no' を True/False に変換
    )

    # m_address 用のデータ (m_account_idは後で取得)
    address_data = (
        # account_id を格納するプレースホルダ
        all_data.get('zip'),
        all_data.get('pref'),
        all_data.get('address1'),
        all_data.get('address2'),
        all_data.get('address3'),
        # ... 他のm_addressの項目
    )

    

    #--最終メールアドレスチェック--

     #同一user確認    
    con = None  # データベース接続オブジェクトを初期化
    cur = None  # カーソルオブジェクトを初期化
    
    # 参考コードをここに応用します
    sql = "SELECT * FROM m_account WHERE mail = %s;"
    
    # connect_db() はご自身の環境で定義されているDB接続関数と想定しています
    con = connect_db() 
    cur = con.cursor(dictionary=True)
    
    # フォームから受け取ったメールアドレスをプレースホルダ(%s)に渡します
    # (account['mail'],) のようにカンマを付けてタプルにすることが重要です
    cur.execute(sql, (all_data['mail'],)) 
    
    # fetchone() で結果を1件取得します
    userExist = cur.fetchone()
    
    # existing_user が None でない場合 ＝ データが取得できた ＝ 既に使用されている
    if userExist:
        #all_data['mail'] "このセッションのメールアドレスは既に使用されている。"
        # エラーなので、テンプレートをレンダリングして処理を終了します

        cur.close()
        con.close()
        error = {}
        error_same = {}

        return render_template('login/new_account.html', error=error, error_same=error_same)



    cur.close()
    con.close()

    #--db登録--


    con = None  # データベース接続オブジェクトを初期化
    cur = None  # カーソルオブジェクトを初期化

    con = connect_db()
    cur = con.cursor()
    # 3. m_account への登録 (まず親テーブルから)
    sql_account = """
    INSERT INTO m_account 
    (mail, password, userName, lastName, firstName, lastNameKana, firstNameKana, birthday, tel, smoker, profileImage)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'default_profile.jpg');
    """
    cur.execute(sql_account, account_data)
    con.commit()

    # 4. 登録されたアカウントのIDを取得 (m_addressで必要)
    new_account_id = cur.lastrowid

    # 5. m_address への登録 (子テーブル)
    sql_address = """
        INSERT INTO m_address 
        (account_id, zip, pref, address1, address2, address3)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    # account_id を address_data の先頭に追加して実行
    full_address_data = (new_account_id,) + address_data
    cur.execute(sql_address, full_address_data)
    con.commit()

    #アカウントIDを取得
    user_id = new_account_id


    # 本人確認画像アップロード処理
    if request.method == 'POST':
        # 実際にはセッションや認証情報から取得するユーザーID
        # 例: user_id = session.get('user_id') 
        # user_id = 101 # ★ 実際のユーザーIDに置き換えてください

        # 1. DB接続を確立
        con = None
        cur = None
        try:
            con = connect_db()
            cur = con.cursor()
        except mysql.connector.Error as err:
            return render_template('login/identity_verification.html', message=f"DB接続エラー: {err}")

        # 2. 保存先のディレクトリ準備
        upload_path = os.path.join(UPLOADS_RELATIVE_PATH)
        os.makedirs(upload_path, exist_ok=True)
        
        uploaded_files = {
            'front_image': request.files.get('front_image'),
            'back_image': request.files.get('back_image')
        }
        
        db_updates = {} # DB更新用のファイル名を保持
        messages = []
        is_error = False

        # 3. ファイルの保存処理
        for file_key, file in uploaded_files.items():
            if file and file.filename != '':
                if allowed_file(file.filename):
                    original_filename = secure_filename(file.filename)
                    extension = original_filename.rsplit('.', 1)[1].lower()
                    
                    # DBのカラム名に対応する変数名を設定
                    db_column_name = 'identifyfrontImg' if file_key == 'front_image' else 'identifybackImg'

                    # 独自のファイル名を作成 (例: 101_front_image.jpg)
                    timestamp = int(datetime.now().timestamp() * 1000)
                    new_filename = f"{user_id}_{file_key}_{timestamp}.{extension}"
                    save_path = os.path.join(upload_path, new_filename)

                    
                    try:
                        # ★ ファイルをサーバーに保存
                        file.save(save_path)
                        messages.append(f"{file_key}のアップロード成功。")
                        
                        # DB更新用にファイル名を記録
                        db_updates[db_column_name] = new_filename

                    except Exception as e:
                        messages.append(f"ファイルの保存中にエラーが発生しました: {e}")
                        is_error = True
                        break # ファイル保存エラーが発生したら次のループに進まず抜ける
                        
                else:
                    messages.append(f"{file_key}のファイル形式が無効です。")
                    is_error = True
                    break

        # 4. データベースの更新処理
        if not is_error and db_updates:
            # 更新するカラムと値を動的に構築
            update_clauses = [f"{col} = %s" for col in db_updates.keys()]
            update_sql = f"UPDATE m_account SET {', '.join(update_clauses)} WHERE id = %s"
            
            # パラメータリスト (ファイル名 + ユーザーID)
            params = list(db_updates.values())
            params.append(user_id)
            
            try:
                # ★ DBにファイル名を保存
                cur.execute(update_sql, tuple(params))
                con.commit()
                messages.append("データベースのファイル名情報が更新されました。")
                
            except mysql.connector.Error as err:
                messages.append(f"DB更新エラー: {err}")
                is_error = True
            finally:
                if con and con.is_connected():
                    cur.close()
                    con.close()
            

        # 5. 結果の反映
        if is_error:
            # エラーが発生した場合は、エラーメッセージを渡してレンダリング
            return render_template('login/verification.html', message="アップロードまたはDB更新に失敗しました。", result_messages=messages)
        else:

            
            # 登録完了したのでセッションデータを削除
            session.pop('registration_data', None)
            # 成功した場合は、確認完了ページなどにリダイレクト
            return render_template('login/registration_complete.html')

    # GETリクエストの場合
    return render_template('login/verification.html')
#

#DB設定------------------------------------------------------------------------------------------------------------------------------------------------------------------
def connect_db():
    con=mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = '',
        db ='db_subkari'
    )
    return con
    


#password-reset----------------------------------------------------------------------------------------------------------------------------------------------------------

@login_bp.route('/password-reset', methods=['GET'])
def password_reset():
    # 初期表示用に空の辞書を渡す
    error = None
    success = None
    message = None
    return render_template('login/forgot_password.html', error=error, success=success,message = message)



# パスワード再設定画面の遷移
@login_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    email_address = request.form.get('email')

    #メールアドレスが登録されているものか確かめる
     #同一user確認    
    con = None  # データベース接続オブジェクトを初期化
    cur = None  # カーソルオブジェクトを初期化
    
    # 参考コードをここに応用します
    sql = "SELECT * FROM m_account WHERE mail = %s;"
    
    # connect_db() はご自身の環境で定義されているDB接続関数と想定しています
    con = connect_db() 
    cur = con.cursor(dictionary=True)
    
    # フォームから受け取ったメールアドレスをプレースホルダ(%s)に渡します
    cur.execute(sql, (email_address,)) 
    
    # fetchone() で結果を1件取得します
    userExist = cur.fetchone()
    
    # existing_user が None の場合 ＝ データ取得できない ＝ 登録されていない
    if   userExist == None:
        
        # エラーなので、テンプレートをレンダリングして処理を終了します

        cur.close()
        con.close()
        message = "このメールアドレスは登録されていません"

        return render_template('login/forgot_password.html', message = message)
    


    #登録されていたら、セッションにメールアドレスを保存
    session['reset_email'] = email_address

    cur.close()
    con.close()

    return render_template('login/password_reset.html')




@login_bp.route('/password-reset/complete', methods=['POST'])
def reset_password():
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    error = None
    success = None

    # バリデーション
    if not password or not password_confirm:
        error = "パスワードを入力してください。"
    elif password != password_confirm:
        error = "パスワードが一致しません。"
    elif len(password) < 8:
        error = "パスワードは8文字以上で入力してください。"


    if error:
        #エラーがある場合フォームテンプレートに戻す
        return render_template('login/password_reset.html', error=error, success=success)

    else:
        email_address =  session['reset_email']

        success = "パスワードを更新しました。"
        # 実際にはここでDBにパスワードを更新
        con = None  # データベース接続オブジェクトを初期化
        cur = None  # カーソルオブジェクトを初期化

        try:
            con = connect_db() 
            cur = con.cursor()
            
            # パスワードを更新するSQL
            sql = "UPDATE m_account SET password = %s WHERE mail = %s;"
            
            # DBにハッシュ化されたパスワードとメールアドレスを渡す
            cur.execute(sql, (password, email_address)) 
            con.commit()
            
            # 4. 成功処理: セッションをクリア
            session.pop('reset_email', None)

            return render_template('login/password_update.html')

        except mysql.connector.Error as err:
            print(f"データベースエラー: {err}")

        finally:
            if con and con.is_connected():
                cur.close()
                con.close()






#メールアドレス忘れ画面の遷移
@login_bp.route('/forgot_email', methods=['GET'])
def forgot_email():


    return render_template('login/forgot_email.html')


#本来ならここで入力された電話番号にSMSをおくる処理
@login_bp.route('/email_sent/success', methods=['POST'])
def email_sent_success():

    #セッションに電話番号を登録する



    #dbに登録されている電話番号があるか確かめる

    #登録されていなかったら、エラーメッセージを渡す


    #SMSにメールアドレスを送信する



    return redirect(url_for('login.email_sent'))



#メールアドレス送信完了表示処理
@login_bp.route('/email_sent', methods=['GET'])
def email_sent():


    return render_template('login/email_sent.html')


#メール再送処理
@login_bp.route('/email_resend', methods=['GET'])
def email_resend():

    #セッション使う


    #再送したメッセージをわたす。

    return render_template('login/email_sent.html')








