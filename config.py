# ==========================================================
# Filename      : config.py
# Descriptions  : 設定ファイル
# ==========================================================
import os
from datetime import timedelta

class Config:
    # Flaskのセッション機能や特定の拡張機能で暗号化キーとして使用される
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'seucrber_tkikeays_ih28'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=240)
