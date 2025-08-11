"""
MCP 服務橋梁 API（簡化版）
"""

from flask import request
from flask_restful import Resource

from utils.response_helpers import create_error_response, create_success_response


class MCPServiceAPI(Resource):
    def post(self):
        """處理 MCP 服務請求"""
        try:
            data = request.get_json()
            action = data.get("action")
            message = data.get("message", "")

            if action == "get_question":
                return self._handle_get_question()
            elif action == "analyze_answer":
                return self._handle_analyze_answer(data)
            elif action == "get_standard_answer":
                return self._handle_get_standard_answer(data)
            else:
                return create_error_response("不支援的動作", status_code=400)

        except Exception as e:
            return create_error_response(f"MCP 服務失敗: {str(e)}", status_code=400)

    def _handle_get_question(self):
        """處理獲取問題請求"""
        return create_success_response(
            data={
                "question": "請介紹您最熟悉的程式語言及其應用場景",
                "category": "技術能力",
                "difficulty": "中等",
                "source": "MCP 服務",
            }
        )

    def _handle_analyze_answer(self, data):
        """處理答案分析請求"""
        user_answer = data.get("user_answer", "")
        question = data.get("question", "")
        standard_answer = data.get("standard_answer", "")

        return create_success_response(
            data={
                "score": 85,
                "grade": "良好",
                "similarity": "80%",
                "feedback": "回答基本正確，但可以更具體一些",
                "standard_answer": standard_answer or "標準答案未提供",
            }
        )

    def _handle_get_standard_answer(self, data):
        """處理獲取標準答案請求"""
        question = data.get("question", "")

        return create_success_response(
            data={
                "question": question,
                "standard_answer": "這是一個標準答案範例",
                "source": "MCP 服務",
            }
        )
