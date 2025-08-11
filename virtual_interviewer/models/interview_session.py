"""
面試會話資料庫模型
"""

from datetime import datetime

from .user import db


class InterviewSession(db.Model):
    """面試會話模型"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    session_data = db.Column(db.Text)  # JSON格式儲存對話內容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        """轉換為字典格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_data": self.session_data,
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else None
            ),
            "updated_at": (
                self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.updated_at
                else None
            ),
        }
