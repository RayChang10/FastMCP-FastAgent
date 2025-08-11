"""
用戶 API 端點
"""

from datetime import datetime

from flask import request
from flask_restful import Resource

from models import Skill, User, WorkExperience, db
from utils.response_helpers import create_error_response, create_success_response
from utils.validators import (
    validate_skill_data,
    validate_user_data,
    validate_work_experience_data,
)


class UserAPI(Resource):
    def post(self):
        """創建新用戶履歷"""
        try:
            data = request.get_json()

            # 驗證用戶資料
            is_valid, errors = validate_user_data(data)
            if not is_valid:
                return create_error_response(
                    f"資料驗證失敗: {'; '.join(errors)}", status_code=400
                )

            # 創建用戶
            user = User(
                name=data.get("name"),
                desired_position=data.get("desired_position"),
                desired_field=data.get("desired_field"),
                desired_location=data.get("desired_location"),
                introduction=data.get("introduction"),
                keywords=data.get("keywords"),
            )

            db.session.add(user)
            db.session.flush()  # 取得user.id

            # 創建工作經驗
            work_experiences = data.get("work_experiences", [])
            for exp_data in work_experiences:
                # 驗證工作經驗資料
                is_valid, errors = validate_work_experience_data(exp_data)
                if not is_valid:
                    continue  # 跳過無效的資料

                experience = WorkExperience(
                    user_id=user.id,
                    company_name=exp_data.get("company_name"),
                    industry_type=exp_data.get("industry_type"),
                    work_location=exp_data.get("work_location"),
                    position_title=exp_data.get("position_title"),
                    position_category_1=exp_data.get("position_category_1"),
                    position_category_2=exp_data.get("position_category_2"),
                    start_date=(
                        datetime.strptime(exp_data.get("start_date"), "%Y-%m-%d").date()
                        if exp_data.get("start_date")
                        else None
                    ),
                    end_date=(
                        datetime.strptime(exp_data.get("end_date"), "%Y-%m-%d").date()
                        if exp_data.get("end_date")
                        else None
                    ),
                    job_description=exp_data.get("job_description"),
                    job_skills=exp_data.get("job_skills"),
                    salary=exp_data.get("salary"),
                    salary_type=exp_data.get("salary_type"),
                    management_responsibility=exp_data.get("management_responsibility"),
                )
                db.session.add(experience)

            # 創建技能
            skills = data.get("skills", [])
            for skill_data in skills:
                # 驗證技能資料
                is_valid, errors = validate_skill_data(skill_data)
                if not is_valid:
                    continue  # 跳過無效的資料

                skill = Skill(
                    user_id=user.id,
                    skill_name=skill_data.get("skill_name"),
                    skill_description=skill_data.get("skill_description"),
                )
                db.session.add(skill)

            db.session.commit()

            return create_success_response(
                data={"user_id": user.id}, message="履歷建立成功", status_code=201
            )

        except Exception as e:
            db.session.rollback()
            return create_error_response(f"建立履歷失敗: {str(e)}", status_code=400)

    def get(self, user_id=None):
        """取得用戶履歷資料"""
        try:
            if user_id:
                user = User.query.get_or_404(user_id)

                work_experiences = [exp.to_dict() for exp in user.work_experiences]
                skills = [skill.to_dict() for skill in user.skills]

                user_data = user.to_dict()
                user_data["work_experiences"] = work_experiences
                user_data["skills"] = skills

                return create_success_response(data=user_data)
            else:
                users = User.query.all()
                users_data = [user.to_dict() for user in users]

                return create_success_response(data=users_data)

        except Exception as e:
            return create_error_response(f"取得履歷資料失敗: {str(e)}", status_code=400)
