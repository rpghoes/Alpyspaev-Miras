from fastapi import Depends, HTTPException, status
from models import User
from main import get_db
from auth import get_current_user

def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Operation requires {required_role} privileges"
            )
        return current_user
    return role_checker
