from typing import Any, Dict

def standard_response(status: int, message: str, data: Any = None) -> Dict:
    return {
        "status": status,
        "message": message,
        "data": data
    }
