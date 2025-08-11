"""
資料庫模型模組
包含所有資料庫模型定義
"""

from flask_sqlalchemy import SQLAlchemy

# 創建資料庫實例
db = SQLAlchemy()

from .interview_session import InterviewSession
from .skill import Skill
from .user import User
from .work_experience import WorkExperience

__all__ = ["User", "WorkExperience", "Skill", "InterviewSession", "db"]
