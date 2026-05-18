from core.modules import Module

module = Module(
    active=True,
    name="auth",
    router_prefix="auth",
    router_tags=["auth"],
)