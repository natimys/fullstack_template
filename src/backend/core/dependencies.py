from fastapi import Depends, HTTPException

from core.enums import UserRole
from core.security import jwt_security
from modules.users.dependencies import get_user_service
from modules.users.service import UserService


def require_role(*roles: UserRole):
    async def dependency(
        payload = Depends(jwt_security.access_token_required),
        user_service: UserService = Depends(get_user_service),
    ):
        user = await user_service.get_user_by_id(int(payload.sub))
        if user.role not in roles:
            raise HTTPException(status_code=403)
        return user
    return dependency
