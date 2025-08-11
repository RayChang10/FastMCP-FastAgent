"""
面試 API 端點（簡化版）
"""

from fast_agent_bridge import (
    analyze_answer,
    analyze_intro,
    clear_all_user_data,
    clear_collected_intro,
    get_collected_intro,
    get_question,
    intro_collector,
)
from flask import request
from flask_restful import Resource

from models import InterviewSession, db
from services.state_manager import InterviewState, InterviewStateManager
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

            # 檢查是否為重置請求
            if user_message.lower() in [
                "重新開始",
                "重新來過",
                "重新面試",
                "重來",
                "restart",
                "reset",
            ]:
                return self._handle_reset_request(user_id)

            # 獲取當前狀態
            current_state = self.state_manager.get_user_state(user_id)

            # 檢查狀態轉換
            state_changed = self.state_manager.transition_state(user_id, user_message)
            if state_changed:
                # 狀態轉換後，重新獲取最新狀態
                current_state = self.state_manager.get_user_state(user_id)
                print(f"🔄 狀態已轉換，新狀態: {current_state.value}")

            # 根據最新狀態處理訊息
            ai_response = self._process_message_by_state(
                user_message, current_state, user_id
            )

            # 處理過程中可能更新了狀態（例如分析完成自動進入面試），因此再次獲取當前狀態
            current_state = self.state_manager.get_user_state(user_id)

            # 儲存對話記錄
            session_data = {
                "user_message": user_message,
                "ai_response": ai_response,
                "current_state": current_state.value,
                "timestamp": "2024-01-01T00:00:00",  # 簡化時間戳
            }

            # 儲存會話（user_id 需為整數，非整數則存 None）
            interview_session = InterviewSession()
            try:
                interview_session.user_id = (
                    int(user_id) if str(user_id).isdigit() else None
                )
            except Exception:
                interview_session.user_id = None
            interview_session.session_data = str(session_data)
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

    def delete(self):
        """處理面試重置請求"""
        try:
            data = request.get_json() or {}
            user_id = data.get("user_id", "default_user")

            return self._handle_reset_request(user_id)

        except Exception as e:
            return create_error_response(f"重置面試失敗: {str(e)}", status_code=500)

    def _handle_reset_request(self, user_id):
        """處理重置請求"""
        try:
            # 1. 清除後端狀態管理器的所有數據
            self.state_manager.clear_user_data(user_id)

            # 2. 清除已收集的自我介紹內容和其他相關數據
            clear_all_user_data(user_id)

            # 3. 清除資料庫中的面試會話記錄
            # 修正：正確處理 user_id 類型不匹配問題
            if str(user_id).isdigit():
                # 如果 user_id 是數字，直接查詢
                InterviewSession.query.filter_by(user_id=int(user_id)).delete()
            else:
                # 如果 user_id 不是數字（如 "default_user"），清除 user_id 為 None 的記錄
                InterviewSession.query.filter_by(user_id=None).delete()

            db.session.commit()

            # 4. 清除其他相關的全局狀態（如果有的話）
            # 這裡可以添加清除其他模組狀態的邏輯

            print(f"🧹 用戶 {user_id} 的所有面試數據已完全清除")

            return create_success_response(
                data={
                    "response": "✅ 面試已完全重置！所有對話記錄、狀態和記憶已清空。請點擊「開始面試」按鈕開始全新的面試。",
                    "session_id": None,
                    "current_state": "waiting",
                    "reset_complete": True,
                }
            )

        except Exception as e:
            db.session.rollback()
            print(f"❌ 重置面試數據失敗: {str(e)}")
            return create_error_response(f"重置面試數據失敗: {str(e)}", status_code=500)

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
            # 移除冗餘的清除調用，避免狀態不一致
            # 這些清除邏輯已經在 _handle_reset_request 中統一處理
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
            """

    def _process_intro_state(self, user_message, user_id):
        """處理自我介紹階段的訊息"""
        lower_message = (user_message or "").lower()
        start_keywords = [
            "開始面試",
            "開始",
            "start_interview",
            "開始練習",
            "準備好了",
            "可以開始了",
        ]
        done_phrases = {
            "介紹完了",
            "介紹完成",
            "我說完了",
            "說完了",
            "完成介紹",
            "結束介紹",
        }

        # 如果剛從等待階段進入自我介紹（收到開始面試相關訊息），給出清晰的自我介紹引導
        if any(keyword in lower_message for keyword in start_keywords):
            return """
🎯 面試開始！

現在進入「自我介紹」階段，請盡量包含以下要素：
- 開場簡介（身份與專業定位）
- 學經歷概述  
- 核心技能與強項
- 代表成果
- 與職缺的連結
- 結語與期待

完成後請輸入：「介紹完了」 以進入分析階段。
            """

        if user_message in done_phrases:
            return "已收到您『自我介紹完成』的指示，將進入分析階段。若未自動切換，請再次輸入：「介紹完了」。"

        if user_message == "介紹完了":
            return """
🎯 **自我介紹完成！**

您的自我介紹內容已收集完畢，現在進入分析階段。

系統正在分析您的自我介紹內容，請稍候...
            """
        else:
            # 收集自我介紹內容，供後續分析使用
            try:
                intro_collector(user_message=user_message, user_id=user_id)
            except Exception:
                pass
            return "✅ 已記錄您的自我介紹內容。請繼續介紹，或說「介紹完了」來開始分析。"

    def _process_intro_analysis_state(self, user_message, user_id):
        """處理自我介紹分析階段：實際呼叫分析並回傳結果，並自動切換到面試階段"""
        # 優先使用已收集的自我介紹內容；若無，退回使用本次訊息
        collected = ""
        try:
            collected = get_collected_intro(user_id)
        except Exception:
            collected = ""

        content_to_analyze = collected.strip() or (user_message or "").strip()
        if not content_to_analyze:
            return "尚未收集到您的自我介紹內容。請先簡要介紹自己，或輸入「重新介紹」重新開始。"

        try:
            result = analyze_intro(user_message=content_to_analyze, user_id=user_id)
            if isinstance(result, dict) and result.get("success"):
                # 在分析完成後，自動切換到面試問答階段
                self.state_manager.set_user_state(user_id, InterviewState.QUESTIONING)

                analysis_text = result.get("result", "📊 自我介紹分析完成。")
                guidance = (
                    "\n\n分析完成，將進入面試階段。系統會在 5 秒後提供第一個問題。"
                )
                return f"{analysis_text}{guidance}"
            # 若回傳非常規格式，直接轉為字串，同時切換到面試階段
            self.state_manager.set_user_state(user_id, InterviewState.QUESTIONING)
            return str(result)
        except Exception as e:
            return f"📊 自我介紹分析出現問題：{str(e)}"

    def _process_questioning_state(self, user_message, user_id):
        """處理面試提問階段的訊息"""
        lower_message = (user_message or "").lower()

        # 取得新題目
        question_request_keywords = {
            "請給我問題",
            "開始問答",
            "開始面試",
            "下一題",
            "下一個問題",
            "給我問題",
        }

        if any(k in lower_message for k in question_request_keywords):
            try:
                result = get_question()
                if isinstance(result, dict) and result.get("success"):
                    qdata = result.get("question_data", {})
                    question_text = qdata.get("question") or ""
                    standard_answer = qdata.get("standard_answer") or ""

                    # 記錄到狀態管理器
                    self.state_manager.set_user_current_question(
                        user_id,
                        question_text,
                        standard_answer,
                        question_data=qdata,
                    )

                    response_text = result.get("result")
                    if not response_text:
                        category = qdata.get("category", "一般")
                        difficulty = qdata.get("difficulty", "中等")
                        response_text = f"🎯 面試問題\n\n類別：{category}\n難度：{difficulty}\n\n問題：{question_text}\n\n請作答，送出後我會立即分析並給出評分。"
                    return response_text
                else:
                    return "抱歉，目前無法取得面試問題，請稍後再試或輸入『請給我問題』重試。"
            except Exception as e:
                return f"取得面試問題失敗：{str(e)}"

        # 分析用戶回答
        current_q = self.state_manager.get_user_current_question(user_id)
        if not current_q:
            return "目前沒有待回答的題目。請先輸入『請給我問題』取得題目。"

        try:
            analysis = analyze_answer(
                user_answer=user_message,
                question=current_q.get("question", ""),
                standard_answer=current_q.get("standard_answer", ""),
            )
            if isinstance(analysis, dict) and analysis.get("success"):
                return analysis.get("result", "分析完成。")
            return str(analysis)
        except Exception as e:
            return f"回答分析失敗：{str(e)}"

    def _process_completed_state(self, user_message, user_id):
        """處理面試完成階段"""
        lower_message = (user_message or "").lower()
        restart_keywords = ["重新開始", "重新來過", "重新面試", "重來", "restart"]

        if any(k in lower_message for k in restart_keywords):
            # 移除冗餘的清除調用，避免狀態不一致
            # 這些清除邏輯已經在 _handle_reset_request 中統一處理
            return "✅ 面試已重置，請點擊「開始面試」按鈕開始新的面試。"
        else:
            return """
✅ **面試已完成**

您的面試總結已經生成完畢。

📋 您現在可以：
- 說「重新開始」開始新的面試
- 查看之前的面試總結

如需重新開始面試，請說「重新開始」。
            """
