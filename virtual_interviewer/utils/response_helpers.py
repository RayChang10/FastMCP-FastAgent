"""
回應輔助工具函數
"""


def create_success_response(data=None, message="操作成功", status_code=200):
    """創建成功回應"""
    response = {"success": True, "message": message, "status_code": status_code}

    if data is not None:
        response["data"] = data

    return response, status_code


def create_error_response(message="操作失敗", error_code=None, status_code=400):
    """創建錯誤回應"""
    response = {"success": False, "message": message, "status_code": status_code}

    if error_code:
        response["error_code"] = error_code

    return response, status_code


def create_api_response(success, data=None, message="", error=None, status_code=200):
    """創建統一的 API 回應格式"""
    response = {"success": success, "message": message, "status_code": status_code}

    if success and data is not None:
        response["data"] = data
    elif not success and error:
        response["error"] = error

    return response, status_code
