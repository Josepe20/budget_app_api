from fastapi.responses import JSONResponse
from typing import TypeVar, Any, Type, List
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta
from datetime import datetime

T = TypeVar("T", bound=BaseModel)

def standard_response(status: int, message: str, data: Any = None, pydantic_model: Type[T] = None) -> JSONResponse:
    # If data is a list of SQLAlchemy models
    if isinstance(data, list) and pydantic_model is not None:
        data = [pydantic_model.model_validate(item).model_dump() for item in data]
        # Convert datetime to ISO format in lists
        for item in data:
            for key, value in item.items():
                if isinstance(value, datetime):
                    item[key] = value.isoformat()
    
    # If data is a single Pydantic model
    elif isinstance(data, BaseModel):
        data = data.model_dump()
        # Convert datetime type fields to ISO format
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()

    # If data is a SQLAlchemy (ORM) model
    elif isinstance(type(data), DeclarativeMeta) and pydantic_model is not None:
        data = pydantic_model.model_validate(data).model_dump()
        # Convert datetime type fields to ISO format
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()

    response_content = {
        "status": status,
        "message": message,
        "data": data
    }

    return JSONResponse(content=response_content, status_code=status)
