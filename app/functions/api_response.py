def standard_response(status: int, message: str, data: dict = None):
    return {
        "status": status,
        "message": message,
        "data": data
    }
