"""
資料驗證工具函數
"""


def validate_user_data(data):
    """驗證用戶資料"""
    errors = []

    # 檢查必填欄位
    if not data.get("name"):
        errors.append("姓名為必填欄位")

    if not data.get("desired_position"):
        errors.append("期望職位為必填欄位")

    # 檢查資料類型
    if data.get("name") and len(data["name"]) > 100:
        errors.append("姓名長度不能超過100個字元")

    if data.get("desired_position") and len(data["desired_position"]) > 200:
        errors.append("期望職位長度不能超過200個字元")

    return len(errors) == 0, errors


def validate_work_experience_data(data):
    """驗證工作經驗資料"""
    errors = []

    if not data.get("company_name"):
        errors.append("公司名稱為必填欄位")

    if not data.get("position_title"):
        errors.append("職位名稱為必填欄位")

    return len(errors) == 0, errors


def validate_skill_data(data):
    """驗證技能資料"""
    errors = []

    if not data.get("skill_name"):
        errors.append("技能名稱為必填欄位")

    return len(errors) == 0, errors
