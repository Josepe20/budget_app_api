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
from typing import TypeVar, Any, Type
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta
from datetime import datetime

T = TypeVar("T", bound=BaseModel)

def standard_response(status: int, message: str, data: Any = None, pydantic_model: Type[T] = None) -> JSONResponse:
    # Si data es una instancia de un modelo Pydantic
    if isinstance(data, BaseModel):
        data = data.model_dump()

    # Si data es una instancia de un modelo SQLAlchemy (ORM)
    elif isinstance(type(data), DeclarativeMeta) and pydantic_model is not None:
        # Convertimos el modelo SQLAlchemy a un modelo Pydantic usando el tipo provisto
        data = pydantic_model.model_validate(data).model_dump()

    # Convertimos los campos de tipo datetime a ISO format si están presentes
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()

    response_content = {
        "status": status,
        "message": message,
        "data": data
    }

    return JSONResponse(content=response_content, status_code=status)





