#!/usr/bin/env python3
"""
虛擬面試顧問 - 啟動腳本
Virtual Interview Consultant - Startup Script
"""

import os
import sys


def setup_python_path():
    """設置 Python 路徑，確保能導入父目錄的模組"""
    try:
        # 獲取當前文件的目錄
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 獲取父目錄（項目根目錄）
        parent_dir = os.path.dirname(current_dir)

        # 將當前目錄添加到 Python 路徑（強制添加）
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        print(f"✅ 當前目錄已在 Python 路徑中: {current_dir}")

        # 將父目錄添加到 Python 路徑
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
            print(f"✅ 已添加父目錄到 Python 路徑: {parent_dir}")

        # 檢查關鍵模組是否可導入
        try:
            import fast_agent_bridge

            print("✅ Fast Agent 橋接模組可導入")
        except ImportError as e:
            print(f"⚠️ Fast Agent 橋接模組導入失敗: {e}")

        try:
            import server

            print("✅ MCP 服務器模組可導入")
        except ImportError as e:
            print(f"⚠️ MCP 服務器模組導入失敗: {e}")

        return True
    except Exception as e:
        print(f"❌ Python 路徑設置失敗: {e}")
        return False


def create_database(app, db):
    """建立資料庫表格"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ 資料庫初始化成功")
    except Exception as e:
        print(f"❌ 資料庫初始化失敗: {e}")
        return False
    return True


def check_requirements():
    """檢查環境需求"""
    try:
        import flask
        import flask_cors
        import flask_restful
        import flask_sqlalchemy

        print("✅ 所有必要套件已安裝")
        return True
    except ImportError as e:
        print(f"❌ 缺少必要套件: {e}")
        print("請執行: pip install -r requirements.txt")
        return False


def main():
    """主啟動函數"""
    print("🚀 虛擬面試顧問啟動中...")
    print("=" * 50)

    # 設置 Python 路徑
    if not setup_python_path():
        print("⚠️ Python 路徑設置失敗，某些功能可能無法使用")

    # 檢查套件
    if not check_requirements():
        sys.exit(1)

    # 導入應用（在設置路徑後）
    from app import app, db

    # 初始化資料庫
    if not create_database(app, db):
        sys.exit(1)

    # 啟動應用
    print(f"🌐 應用程式將在 http://localhost:5000 啟動")
    print("📝 主頁面: http://localhost:5000")
    print("📋 履歷建立: http://localhost:5000/resume")
    print("=" * 50)
    print("按 Ctrl+C 停止應用程式")

    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 應用程式已停止")
    except Exception as e:
        print(f"❌ 應用程式啟動失敗: {e}")


if __name__ == "__main__":
    main()
