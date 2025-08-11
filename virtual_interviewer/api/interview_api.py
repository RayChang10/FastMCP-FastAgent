"""
面試 API 端點（簡化版）
"""

from flask import request
from flask_restful import Resource

from models import InterviewSession, db
from services.state_manager import InterviewStateManager
from utils.response_helpers import create_error_response, create_success_response


class InterviewAPI(Resource):
    def __init__(self):
        self.state_manager = InterviewStateManager()

    def post(self):
        """處理面試對話"""
        try:
            data = request.get_json()
            user_message = data.get("message", "")
            user_id = data.get("user_id", "default_user")

            # 獲取當前狀態
            current_state = self.state_manager.get_user_state(user_id)

            # 檢查狀態轉換
            state_changed = self.state_manager.transition_state(user_id, user_message)
            if state_changed:
                current_state = self.state_manager.get_user_state(user_id)

            # 根據狀態處理訊息
            ai_response = self._process_message_by_state(
                user_message, current_state, user_id
            )

            # 儲存對話記錄
            session_data = {
                "user_message": user_message,
                "ai_response": ai_response,
                "current_state": current_state.value,
                "timestamp": "2024-01-01T00:00:00",  # 簡化時間戳
            }

            interview_session = InterviewSession(
                user_id=user_id, session_data=str(session_data)
            )
            db.session.add(interview_session)
            db.session.commit()

            return create_success_response(
                data={
                    "response": ai_response,
                    "session_id": interview_session.id,
                    "current_state": current_state.value,
                }
            )

        except Exception as e:
            db.session.rollback()
            return create_error_response(f"處理面試對話失敗: {str(e)}", status_code=400)

    def _process_message_by_state(self, user_message, current_state, user_id):
        """根據狀態處理訊息"""
        if current_state.value == "waiting":
            return self._process_waiting_state(user_message)
        elif current_state.value == "intro":
            return self._process_intro_state(user_message, user_id)
        elif current_state.value == "intro_analysis":
            return self._process_intro_analysis_state(user_message, user_id)
        elif current_state.value == "questioning":
            return self._process_questioning_state(user_message, user_id)
        elif current_state.value == "completed":
            return self._process_completed_state(user_message, user_id)
        else:
            return "未知狀態，請重新開始面試。"

    def _process_waiting_state(self, user_message):
        """處理等待開始階段的訊息"""
        lower_message = user_message.lower()
        start_keywords = [
            "開始面試",
            "開始",
            "start_interview",
            "開始練習",
            "準備好了",
            "可以開始了",
        ]

        if any(keyword in lower_message for keyword in start_keywords):
            return """
🎯 面試開始！

歡迎參加智能面試系統！接下來我們將進行以下流程：

1️⃣ **自我介紹階段**：請進行完整的自我介紹
2️⃣ **自我介紹分析**：我會分析您的介紹並給出建議  
3️⃣ **面試問答**：進行技術或行為面試問題
4️⃣ **總結建議**：給出最終的面試表現總結

現在請開始您的自我介紹。請盡量包含以下要素：
- 開場簡介（身份與專業定位）
- 學經歷概述  
- 核心技能與強項
- 代表成果
- 與職缺的連結
- 結語與期待

請開始您的自我介紹：
            """
        else:
            return f"""
👋 您好！歡迎使用智能面試系統！

我是您的AI面試官，準備為您提供專業的模擬面試體驗。

🎯 **面試流程說明**：
1. 自我介紹 → 2. 介紹分析 → 3. 技術問答 → 4. 總結建議

請點擊「開始面試」按鈕，或輸入「開始面試」來開始您的面試之旅！

您說：「{user_message}」
            """

    def _process_intro_state(self, user_message, user_id):
        """處理自我介紹階段的訊息"""
        if user_message == "介紹完了":
            return """
🎯 **自我介紹完成！**

您的自我介紹內容已收集完畢，現在進入分析階段。

系統正在分析您的自我介紹內容，請稍候...
            """
        else:
            return "✅ 已記錄您的自我介紹內容。請繼續介紹，或說「介紹完了」來開始面試。"

    def _process_intro_analysis_state(self, user_message, user_id):
        """處理自我介紹分析階段"""
        return """
📊 **自我介紹分析結果**

您的自我介紹已分析完畢。現在您可以：
- 說「開始面試」進入面試問答階段
- 說「重新介紹」重新進行自我介紹

請告訴我您想要如何繼續？
        """

    def _process_questioning_state(self, user_message, user_id):
        """處理面試提問階段的訊息"""
        return f"""
🎯 **面試問題階段**

您說：「{user_message}」

這是一個很好的回答！我會分析您的回答並給出評分。

請等待系統準備下一題...
        """

    def _process_completed_state(self, user_message, user_id):
        """處理面試完成階段"""
        return """
✅ **面試已完成**

您的面試總結已經生成完畢。

📋 您現在可以：
- 說「重新開始」開始新的面試
- 查看之前的面試總結

如需重新開始面試，請說「重新開始」。
        """
