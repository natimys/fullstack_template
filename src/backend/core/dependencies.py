from fastapi import Depends, HTTPException

from core.enums import UserRole
from core.security import jwt_security


def require_role(*roles: UserRole):
    def dependency(payload=Depends(jwt_security.access_token_required)):
        if payload.role not in roles:
            raise HTTPException(403)
        return payload

    return dependency
