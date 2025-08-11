"""
工作經驗資料庫模型
"""

from datetime import datetime

from .user import db


class WorkExperience(db.Model):
    """工作經驗模型"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    industry_type = db.Column(db.String(100))
    work_location = db.Column(db.String(100))
    position_title = db.Column(db.String(200))
    position_category_1 = db.Column(db.String(100))
    position_category_2 = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    job_description = db.Column(db.Text)
    job_skills = db.Column(db.Text)
    salary = db.Column(db.String(100))
    salary_type = db.Column(db.String(50))
    management_responsibility = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """轉換為字典格式"""
        return {
            "id": self.id,
            "company_name": self.company_name,
            "industry_type": self.industry_type,
            "work_location": self.work_location,
            "position_title": self.position_title,
            "position_category_1": self.position_category_1,
            "position_category_2": self.position_category_2,
            "start_date": (
                self.start_date.strftime("%Y-%m-%d") if self.start_date else None
            ),
            "end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
            "job_description": self.job_description,
            "job_skills": self.job_skills,
            "salary": self.salary,
            "salary_type": self.salary_type,
            "management_responsibility": self.management_responsibility,
        }
