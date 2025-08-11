#!/usr/bin/env python3
"""
測試面試 API 的簡單腳本
"""

import json

import requests


def test_interview_api():
    """測試面試 API"""
    base_url = "http://localhost:5000"

    # 測試開始面試
    print("🧪 測試開始面試...")

    data = {"message": "開始面試", "user_id": "test_user"}

    try:
        response = requests.post(
            f"{base_url}/api/interview",
            json=data,
            headers={"Content-Type": "application/json"},
        )

        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.text}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ API 測試成功！")
            print(f"回應內容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ API 測試失敗！")

    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到應用程式，請確保應用程式正在運行")
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")


if __name__ == "__main__":
    test_interview_api()
