# ==========================================================
# Filename      : app/__init__.py
# Descriptions  : Application Factory
# ==========================================================
from flask import Flask,make_response, render_template,request,session
from config import Config

def create_app():
    # Flaskアプリケーションのインスタンスを作成
    # __name__をappパッケージのパスに設定
    app = Flask(__name__)
    
    # config.pyから設定を読み込む
    app.config.from_object(Config)

    # --- Blueprintの登録 ---
    # viewsパッケージからproductsとauthのBlueprintをインポート
    from .views import top,login,products,seller,dashboard,mypage,deal,userprf,brand_serach
    
    app.register_blueprint(top.top_bp)
    app.register_blueprint(login.login_bp)
    app.register_blueprint(products.products_bp)
    app.register_blueprint(seller.seller_bp)
    app.register_blueprint(dashboard.dashboard_bp)
    app.register_blueprint(mypage.mypage_bp)
    app.register_blueprint(deal.deal_bp)
    app.register_blueprint(userprf.userprf_bp)
    app.register_blueprint(brand_serach.brand_serach_bp)

  

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html'), 500
    
    return app