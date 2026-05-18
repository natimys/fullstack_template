from core.modules import Module

module = Module(
    active=True,
    name="users",
    router_prefix="/users",
    router_tags=["users"],
)