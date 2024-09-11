from datetime import datetime, timezone
from fastapi import HTTPException, status

def validate_active_month(created_at: datetime):
    current_month = datetime.now().month
    current_year = datetime.now().year

    if created_at.month != current_month or created_at.year != current_year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only perform this action in the current active month."
        )