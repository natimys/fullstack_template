from dataclasses import dataclass
import importlib
import pkgutil

from fastapi import FastAPI

import modules

def register_routers(app: FastAPI):
    for _, module_name, ispkg in pkgutil.iter_modules(modules.__path__):
        if not ispkg:
            continue
        try:
            router_module = importlib.import_module(f"modules.{module_name}.router")
            if hasattr(router_module, "router"):
                app.include_router(router_module.router)
                print(f"✅ {module_name} router loaded successfully")
        except ModuleNotFoundError:
            print(f"❌ {module_name} router loading failed")
            continue

@dataclass
class Module:
    active: bool
    name: str
    router_prefix: str
    router_tags: list[str]