from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class Permission(str, Enum):
    AUTH_READ = "auth:read"
    USERS_READ = "users:read"
    USERS_CREATE = "users:create"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"


# Roles inherit permissions from their parents. Validate this graph at import
# time so a newly introduced cycle cannot silently widen or break access.
ROLE_PARENTS: dict[UserRole, tuple[UserRole, ...]] = {
    UserRole.USER: (),
    UserRole.ADMIN: (UserRole.USER,),
}

ROLE_PERMISSIONS: dict[UserRole, frozenset[Permission]] = {
    UserRole.USER: frozenset({Permission.AUTH_READ}),
    UserRole.ADMIN: frozenset(
        {
            Permission.USERS_READ,
            Permission.USERS_CREATE,
            Permission.USERS_UPDATE,
            Permission.USERS_DELETE,
        }
    ),
}


def _role_permissions(role: UserRole, visiting: set[UserRole]) -> frozenset[Permission]:
    if role in visiting:
        raise ValueError(f"Role inheritance cycle detected at {role.value}")
    visiting.add(role)
    permissions = set(ROLE_PERMISSIONS.get(role, ()))
    for parent in ROLE_PARENTS.get(role, ()):
        permissions.update(_role_permissions(parent, visiting))
    visiting.remove(role)
    return frozenset(permissions)


ROLE_PERMISSION_MAP = {role: _role_permissions(role, set()) for role in UserRole}


def has_permission(role: UserRole, permission: Permission) -> bool:
    return permission in ROLE_PERMISSION_MAP[role]
