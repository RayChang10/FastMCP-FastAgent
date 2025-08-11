"""
虛擬人 API 端點（簡化版）
"""

from flask import request
from flask_restful import Resource

from utils.response_helpers import create_error_response, create_success_response


class AvatarAPI(Resource):
    def post(self):
        """虛擬人狀態控制API"""
        try:
            data = request.get_json()
            action = data.get("action")

            if action == "speak":
                return self._handle_speak_action(data)
            elif action == "listen":
                return self._handle_listen_action(data)
            elif action == "emotion":
                return self._handle_emotion_action(data)
            elif action == "idle":
                return self._handle_idle_action(data)
            else:
                return create_error_response("不支援的操作", status_code=400)

        except Exception as e:
            return create_error_response(f"虛擬人控制失敗: {str(e)}", status_code=400)

    def _handle_speak_action(self, data):
        """處理說話動作"""
        text = data.get("text", "")
        return create_success_response(
            data={
                "audio_url": "/api/avatar/audio/latest",
                "lip_sync_data": [],
                "duration": 3.5,
                "emotion": "neutral",
            }
        )

    def _handle_listen_action(self, data):
        """處理聆聽狀態"""
        return create_success_response(
            data={"state": "listening", "animation": "listening_idle", "duration": -1}
        )

    def _handle_emotion_action(self, data):
        """處理表情變化"""
        emotion = data.get("emotion", "neutral")
        intensity = data.get("intensity", 0.5)

        return create_success_response(
            data={
                "emotion": emotion,
                "intensity": intensity,
                "transition_duration": 1.0,
            }
        )

    def _handle_idle_action(self, data):
        """處理待機狀態"""
        return create_success_response(
            data={"state": "idle", "animation": "breathing", "blink_interval": 3.0}
        )
