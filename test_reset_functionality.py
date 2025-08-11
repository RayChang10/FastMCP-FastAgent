#!/usr/bin/env python3
"""
測試面試重置功能
驗證重新開始面試後是否能完全清除之前的內容
"""

import json
import time

import requests


def test_interview_reset():
    """測試面試重置功能"""

    base_url = "http://localhost:5000"
    user_id = "test_user_123"

    print("🧪 開始測試面試重置功能...")

    # 1. 開始面試
    print("\n1️⃣ 開始面試...")
    response = requests.post(
        f"{base_url}/api/interview", json={"message": "開始面試", "user_id": user_id}
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ 面試開始成功: {data['data']['current_state']}")
    else:
        print(f"❌ 面試開始失敗: {response.status_code}")
        return False

    # 2. 進行一些對話
    print("\n2️⃣ 進行對話...")
    messages = [
        "我是測試用戶，有3年Python開發經驗",
        "我熟悉Django、Flask等框架",
        "介紹完了",
    ]

    for i, msg in enumerate(messages, 1):
        response = requests.post(
            f"{base_url}/api/interview", json={"message": msg, "user_id": user_id}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ 對話 {i}: {data['data']['current_state']}")
        else:
            print(f"❌ 對話 {i} 失敗: {response.status_code}")

    # 3. 重置面試
    print("\n3️⃣ 重置面試...")
    response = requests.delete(f"{base_url}/api/interview", json={"user_id": user_id})

    if response.status_code == 200:
        data = response.json()
        if data["data"].get("reset_complete"):
            print("✅ 面試重置成功")
        else:
            print("⚠️ 面試重置可能不完整")
    else:
        print(f"❌ 面試重置失敗: {response.status_code}")
        return False

    # 4. 驗證重置後的狀態
    print("\n4️⃣ 驗證重置後的狀態...")
    response = requests.post(
        f"{base_url}/api/interview", json={"message": "測試訊息", "user_id": user_id}
    )

    if response.status_code == 200:
        data = response.json()
        current_state = data["data"]["current_state"]
        if current_state == "waiting":
            print("✅ 重置後狀態正確: waiting")
        else:
            print(f"⚠️ 重置後狀態不正確: {current_state}")
    else:
        print(f"❌ 驗證重置狀態失敗: {response.status_code}")
        return False

    print("\n🎉 面試重置功能測試完成！")
    return True


def test_multiple_resets():
    """測試多次重置功能"""

    base_url = "http://localhost:5000"
    user_id = "test_user_456"

    print("\n🔄 測試多次重置功能...")

    for i in range(3):
        print(f"\n--- 第 {i+1} 次重置測試 ---")

        # 開始面試
        response = requests.post(
            f"{base_url}/api/interview",
            json={"message": "開始面試", "user_id": user_id},
        )

        if response.status_code == 200:
            print(f"✅ 第 {i+1} 次面試開始成功")
        else:
            print(f"❌ 第 {i+1} 次面試開始失敗")
            continue

        # 進行一些對話
        response = requests.post(
            f"{base_url}/api/interview",
            json={"message": "我是測試用戶", "user_id": user_id},
        )

        if response.status_code == 200:
            print(f"✅ 第 {i+1} 次對話成功")
        else:
            print(f"❌ 第 {i+1} 次對話失敗")

        # 重置面試
        response = requests.delete(
            f"{base_url}/api/interview", json={"user_id": user_id}
        )

        if response.status_code == 200:
            print(f"✅ 第 {i+1} 次重置成功")
        else:
            print(f"❌ 第 {i+1} 次重置失敗")

        # 等待一下
        time.sleep(1)

    print("\n🎉 多次重置測試完成！")


if __name__ == "__main__":
    try:
        # 測試基本重置功能
        success = test_interview_reset()

        if success:
            # 測試多次重置功能
            test_multiple_resets()
        else:
            print("❌ 基本重置功能測試失敗，跳過多次重置測試")

    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器，請確保虛擬面試系統正在運行")
        print("💡 請運行: python run.py")
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
