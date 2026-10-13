from authx import TokenPayload
from fastapi import Depends, HTTPException, status

from core.enums import Permission, UserRole, has_permission
from core.security import jwt_security
from modules.users.dependencies import get_user_service
from modules.users.models import User
from modules.users.service import UserService


async def get_current_user(
    payload: TokenPayload = Depends(jwt_security.access_token_required),
    user_service: UserService = Depends(get_user_service),
) -> User:
    try:
        user_id = int(payload.sub)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = await user_service.get_user_by_id(user_id)
    if (
        user is None
        or not user.is_active
        or getattr(payload, "session_version", None) != user.session_version
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is no longer valid",
        )
    return user


def require_permission(permission: Permission):
    async def check_permission(user: User = Depends(get_current_user)) -> User:
        try:
            role = UserRole(user.role)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Role has no permissions"
            )
        if not has_permission(role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
            )
        return user

    return check_permission
