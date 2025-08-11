"""
面試狀態管理器
"""

from enum import Enum


class InterviewState(Enum):
    """面試狀態枚舉"""

    WAITING = "waiting"  # 等待開始面試
    INTRO = "intro"  # 自我介紹階段
    INTRO_ANALYSIS = "intro_analysis"  # 自我介紹分析階段
    QUESTIONING = "questioning"  # 面試提問階段
    COMPLETED = "completed"  # 面試完成階段


class InterviewStateManager:
    """面試狀態管理器"""

    def __init__(self):
        # 使用類別層級共享狀態，避免每次請求被重置
        # 注意：不要在 __init__ 內重新指派同名實例屬性
        pass

    # 類別層級共享映射：在所有實例與請求之間共享
    session_states = {}
    user_current_questions = {}

    def get_user_state(self, user_id):
        """獲取用戶的當前狀態"""
        if user_id not in self.session_states:
            self.session_states[user_id] = InterviewState.WAITING
        return self.session_states[user_id]

    def set_user_state(self, user_id, state):
        """設置用戶的狀態"""
        self.session_states[user_id] = state
        print(f"🔄 用戶 {user_id} 狀態變更為: {state.value}")

    def set_user_current_question(
        self, user_id, question, standard_answer, question_data=None
    ):
        """設置用戶當前問題"""
        self.user_current_questions[user_id] = {
            "question": question,
            "standard_answer": standard_answer,
            "question_data": question_data,
        }
        print(f"📝 用戶 {user_id} 當前問題已設置: {question[:50]}...")

    def get_user_current_question(self, user_id):
        """獲取用戶當前問題"""
        return self.user_current_questions.get(user_id, None)

    def clear_user_data(self, user_id):
        """清空用戶的所有狀態數據"""
        if user_id in self.session_states:
            del self.session_states[user_id]
        if user_id in self.user_current_questions:
            del self.user_current_questions[user_id]
        print(f"🧹 用戶 {user_id} 的所有狀態數據已清空")

    def transition_state(self, user_id, user_message):
        """根據用戶訊息判斷是否需要狀態轉換"""
        lower_message = user_message.lower()
        current_state = self.get_user_state(user_id)

        # 從 WAITING 轉換到 INTRO（按下開始面試按鈕）
        if current_state == InterviewState.WAITING:
            start_keywords = [
                "開始面試",
                "開始",
                "start_interview",
                "開始練習",
                "準備好了",
                "可以開始了",
            ]
            if any(keyword in lower_message for keyword in start_keywords):
                self.set_user_state(user_id, InterviewState.INTRO)
                return True

        # 從 INTRO 轉換到 INTRO_ANALYSIS（完成自我介紹）
        elif current_state == InterviewState.INTRO:
            # 接受多個同義詞
            done_phrases = {
                "介紹完了",
                "介紹完成",
                "我說完了",
                "說完了",
                "完成介紹",
                "結束介紹",
            }
            if user_message in done_phrases:
                self.set_user_state(user_id, InterviewState.INTRO_ANALYSIS)
                return True

        # 從 INTRO_ANALYSIS 轉換到 QUESTIONING（用戶要求開始面試）
        elif current_state == InterviewState.INTRO_ANALYSIS:
            start_interview_keywords = [
                "開始面試",
                "開始問答",
                "進入面試",
                "開始提問",
                "給我問題",
            ]
            if any(keyword in lower_message for keyword in start_interview_keywords):
                self.set_user_state(user_id, InterviewState.QUESTIONING)
                return True

        # 從 QUESTIONING 轉換到 COMPLETED（用戶要求退出）
        elif current_state == InterviewState.QUESTIONING:
            exit_keywords = ["退出", "結束", "完成", "不想繼續", "停止"]
            if any(keyword in lower_message for keyword in exit_keywords):
                self.set_user_state(user_id, InterviewState.COMPLETED)
                return True

        # 重新開始的情況
        restart_keywords = ["重新開始", "重新來過", "重新面試", "重來"]
        if any(keyword in lower_message for keyword in restart_keywords):
            self.set_user_state(user_id, InterviewState.WAITING)
            return True

        return False

    def get_system_prompt(self, state: InterviewState) -> str:
        """根據當前狀態獲取系統提示詞"""
        if state == InterviewState.WAITING:
            return """
你現在是一個智能面試官助手，目前處於「等待開始」階段。

- 歡迎用戶，說明面試流程
- 等待用戶按下「開始面試」按鈕
- 在未開始面試前，可以進行一般對話和系統介紹
- 不要主動開始面試流程
"""
        elif state == InterviewState.INTRO:
            return """
你現在是一個面試官助手，目前進行到「自我介紹階段」。

- 請明確要求用戶進行完整的自我介紹
- 不論用戶說什麼，都當成是自我介紹內容
- 收集用戶的自我介紹內容，但不要分析或評論
- 使用 `intro_collector` 工具將內容儲存
- 引導用戶說出完整的自我介紹（開場、學經歷、技能、成果、職缺連結、結語）
- 當用戶說「介紹完了」或類似話語時，進入分析階段
"""
        elif state == InterviewState.INTRO_ANALYSIS:
            return """
你現在是一個面試官助手，目前進行到「自我介紹分析階段」。

- 使用 `analyze_intro` 工具分析用戶的自我介紹
- 依據6個標準進行分析：開場簡介、學經歷概述、核心技能與強項、代表成果、與職缺的連結、結語與期待
- 指出缺失的部分並給出具體建議
- 分析完成後自動進入面試提問階段
"""
        elif state == InterviewState.QUESTIONING:
            return """
你現在是一個面試官助手，目前進行到「面試提問與回答階段」。

- 使用 `get_question` 工具獲取面試題目並給出
- 用戶的回答使用 `analyze_answer` 工具分析並評分
- 顯示標準答案和評分結果
- 自動進入下一題，除非用戶說「退出」或「結束」
- 每次回答後都要提醒：「除非說退出，否則會繼續下一題」
- 完成多個題目後可進入完成階段
"""
        elif state == InterviewState.COMPLETED:
            return """
你現在是一個面試官助手，目前進行到「面試完成階段」。

- 使用 `generate_final_summary` 工具統合整個面試過程
- 包含自我介紹分析、面試表現、整體建議
- 給出專業的面試總結和改進建議
- 感謝用戶參與面試
"""
        else:
            return "你是一個面試官助手。"

    def get_available_tools(self, state: InterviewState):
        """根據當前狀態獲取可用工具"""
        if state == InterviewState.WAITING:
            return ["general_chat"]
        elif state == InterviewState.INTRO:
            return ["intro_collector"]
        elif state == InterviewState.INTRO_ANALYSIS:
            return ["analyze_intro"]
        elif state == InterviewState.QUESTIONING:
            return ["get_question", "analyze_answer"]
        elif state == InterviewState.COMPLETED:
            return ["generate_final_summary"]
        else:
            return []
