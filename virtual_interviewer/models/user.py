"""
用戶資料庫模型
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """用戶模型"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    desired_position = db.Column(db.String(200))
    desired_field = db.Column(db.String(100))
    desired_location = db.Column(db.String(100))
    introduction = db.Column(db.Text)
    keywords = db.Column(db.Text)  # JSON格式儲存
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯
    work_experiences = db.relationship(
        "WorkExperience", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    skills = db.relationship(
        "Skill", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        """轉換為字典格式"""
        return {
            "id": self.id,
            "name": self.name,
            "desired_position": self.desired_position,
            "desired_field": self.desired_field,
            "desired_location": self.desired_location,
            "introduction": self.introduction,
            "keywords": self.keywords,
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else None
            ),
        }
