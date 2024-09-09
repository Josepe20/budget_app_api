""" from typing import Any, Dict

def standard_response(status: int, message: str, data: Any = None) -> Dict:
    return {
        "status": status,
        "message": message,
        "data": data
    } """


from fastapi.responses import JSONResponse
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def standard_response(status: int, message: str, data: T = None) -> JSONResponse:
    # Use model_dump_json to convert data into JSON if it is a Pydantic model
    response_content = {
        "status": status,
        "message": message,
        "data": data.model_dump() if isinstance(data, BaseModel) else data  # Ensuring the data is serializable
    }
    return JSONResponse(content=response_content, status_code=status)



