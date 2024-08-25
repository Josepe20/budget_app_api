from pydantic import BaseModel
from typing import Optional, Dict, Any

class StandardResponse(BaseModel):
    status: int
    message: str
    data: Optional[Dict[str, Any]] = None