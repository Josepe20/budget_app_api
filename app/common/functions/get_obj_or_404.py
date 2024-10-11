from fastapi import HTTPException, status
from typing import TypeVar, Any, Type, List

T = TypeVar('T')  # Para el tipado genérico

def get_object_or_404(obj: T, error_message: str = 'Object not found') -> T:
    """Devuelve el objeto si existe, de lo contrario lanza un 404."""
    if not obj:
        print(error_message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
    return obj

def get_list_or_404(objects: List[T], error_message: str = 'No objects found') -> List[T]:
    """Devuelve la lista si tiene elementos, de lo contrario lanza un 404."""
    if not objects:  
        print(error_message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
    return objects
