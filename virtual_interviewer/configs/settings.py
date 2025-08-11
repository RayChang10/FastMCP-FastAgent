"""
應用程式配置設定
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """基礎配置類別"""

    SECRET_KEY = os.environ.get("SECRET_KEY", "virtual_interview_consultant_2024")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///virtual_interview.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OpenAI 配置
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # 應用程式配置
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
    PORT = int(os.environ.get("FLASK_PORT", "5000"))

    # 跨域配置
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

    # 檔案上傳配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

    # 日誌配置
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = os.environ.get("LOG_FILE", "app.log")
