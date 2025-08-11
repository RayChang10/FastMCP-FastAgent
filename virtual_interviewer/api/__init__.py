"""
API 路由模組
包含所有 API 端點定義
"""

from .avatar_api import AvatarAPI
from .fast_agent_api import FastAgentAPI
from .interview_api import InterviewAPI
from .mcp_api import MCPServiceAPI
from .speech_api import SpeechAPI
from .user_api import UserAPI

__all__ = [
    "UserAPI",
    "InterviewAPI",
    "FastAgentAPI",
    "AvatarAPI",
    "SpeechAPI",
    "MCPServiceAPI",
    "register_blueprints",
]


def register_blueprints(api):
    """註冊所有 API 藍圖"""
    api.add_resource(UserAPI, "/api/users", "/api/users/<int:user_id>")
    api.add_resource(InterviewAPI, "/api/interview")
    api.add_resource(FastAgentAPI, "/api/fast-agent")
    api.add_resource(AvatarAPI, "/api/avatar/control")
    api.add_resource(SpeechAPI, "/api/speech")
    api.add_resource(MCPServiceAPI, "/api/mcp")
