"""
語音處理 API 端點（簡化版）
"""

from flask import request
from flask_restful import Resource

from utils.response_helpers import create_error_response, create_success_response


class SpeechAPI(Resource):
    def post(self):
        """語音處理綜合API"""
        try:
            data = request.get_json()
            action = data.get("action")

            if action == "transcribe":
                return self._handle_transcription(data)
            elif action == "synthesize":
                return self._handle_synthesis(data)
            elif action == "realtime":
                return self._handle_realtime(data)
            else:
                return create_error_response("不支援的語音處理動作", status_code=400)

        except Exception as e:
            return create_error_response(f"語音處理失敗: {str(e)}", status_code=400)

    def _handle_transcription(self, data):
        """處理語音轉文字請求"""
        return create_success_response(
            data={
                "action": "transcribe",
                "redirect_to": "/api/stt",
                "message": "請使用POST /api/stt上傳音頻檔案",
            }
        )

    def _handle_synthesis(self, data):
        """處理文字轉語音請求"""
        return create_success_response(
            data={
                "action": "synthesize",
                "redirect_to": "/api/tts/generate",
                "message": "請使用POST /api/tts/generate進行語音合成",
            }
        )

    def _handle_realtime(self, data):
        """處理即時語音互動"""
        return create_success_response(
            data={
                "action": "realtime",
                "websocket_url": "ws://localhost:5000/speech-realtime",
                "session_id": "speech_session_123",
            }
        )
