"""
重構後的虛擬面試系統主應用
精簡版，主要負責應用程式初始化和路由註冊
"""

import os
import sys
from pathlib import Path

# 添加父目錄到路徑
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# 添加當前目錄到路徑
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api

# 直接導入配置文件
import configs.settings
from api import register_blueprints

Config = configs.settings.Config

# 導入重構後的模組
from models import db


def register_web_routes(app):
    """註冊網頁路由"""

    @app.route("/")
    def index():
        """主頁面"""
        return render_template("index.html")

    @app.route("/resume")
    def resume():
        """履歷輸入頁面"""
        return render_template("resume.html")

    @app.route("/test")
    def test():
        """面試系統測試頁面"""
        return render_template("browser_test.html")


def create_app():
    """創建 Flask 應用程式"""
    app = Flask(__name__)

    # 載入配置
    app.config.from_object(Config)

    # 初始化擴展
    db.init_app(app)
    CORS(app)
    api = Api(app)

    # 註冊 API 路由
    register_blueprints(api)

    # 註冊網頁路由
    register_web_routes(app)

    return app


# 創建應用程式實例
app = create_app()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
