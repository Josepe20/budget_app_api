from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

T = TypeVar("T", bound=BaseModel)

class StandardResponse(Generic[T], BaseModel):
    status: int
    message: str
    data: Optional[T] = None

    class Config:
        orm_mode = True
        model_config = {"from_attributes": True}

