from typing import Any, Dict

def standard_response(status: int, message: str, data: Any = None) -> Dict:
    return {
        "status": status,
        "message": message,
        "data": data
    }

""" from fastapi.responses import JSONResponse
from typing import Any

def standard_response(status: int, message: str, data: Any = None) -> JSONResponse:
    response_content = {
        "status": status,
        "message": message,
        "data": data
    }
    return JSONResponse(content=response_content, status_code=status) """

