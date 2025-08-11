"""
Fast Agent API 端點
"""

from flask import request
from flask_restful import Resource

from utils.response_helpers import create_error_response, create_success_response

# 嘗試導入 Fast Agent 橋接模組
try:
    import os
    import sys

    # 獲取當前文件的目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 獲取父目錄（項目根目錄）
    parent_dir = os.path.dirname(current_dir)

    # 將父目錄添加到 Python 路徑
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    from fast_agent_bridge import call_fast_agent_function

    FAST_AGENT_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Fast Agent 橋接模組導入失敗: {e}")
    FAST_AGENT_AVAILABLE = False


class FastAgentAPI(Resource):
    def post(self):
        """Fast Agent 專用 API 端點"""
        try:
            if not FAST_AGENT_AVAILABLE:
                return create_error_response("Fast Agent 模組不可用", status_code=503)

            data = request.get_json()
            function_name = data.get("function")
            arguments = data.get("arguments", {})

            if not function_name:
                return create_error_response("缺少 function 參數", status_code=400)

            # 調用 Fast Agent 函數
            result = call_fast_agent_function(function_name, **arguments)

            if result.get("success"):
                return create_success_response(
                    data=result.get("result", ""), message="Fast Agent 調用成功"
                )
            else:
                return create_error_response(
                    message=f"Fast Agent 調用失敗: {result.get('error', '未知錯誤')}",
                    status_code=400,
                )

        except Exception as e:
            return create_error_response(
                f"Fast Agent API 失敗: {str(e)}", status_code=400
            )
