""" 
from typing import Any, Dict

def standard_response(status: int, message: str, data: Any = None) -> Dict:
    return {
        "status": status,
        "message": message,
        "data": data
    } 
"""


from fastapi.responses import JSONResponse
from typing import TypeVar, Any
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T", bound=BaseModel)

def standard_response(status: int, message: str, data: T = None) -> JSONResponse:
    # Manually serialize datetime fields if present
    if isinstance(data, BaseModel):
        data_dict = data.model_dump()
        for key, value in data_dict.items():
            if isinstance(value, datetime):
                data_dict[key] = value.isoformat()  # Convert datetime to ISO format
    else:
        data_dict = data

    response_content = {
        "status": status,
        "message": message,
        "data": data_dict
    }

    return JSONResponse(content=response_content, status_code=status)




