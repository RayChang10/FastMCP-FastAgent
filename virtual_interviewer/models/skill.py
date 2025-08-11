"""
技能資料庫模型
"""

from datetime import datetime

from . import db


class Skill(db.Model):
    """技能模型"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    skill_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """轉換為字典格式"""
        return {
            "id": self.id,
            "skill_name": self.skill_name,
            "skill_description": self.skill_description,
        }
