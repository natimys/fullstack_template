import importlib
import pkgutil

import uvicorn
from fastapi import FastAPI

import modules
app = FastAPI()

def register_routers():
    for _, module_name, ispkg in pkgutil.iter_modules(modules.__path__):
        if not ispkg:
            continue
        try:
            router_module = importlib.import_module(f"modules.{module_name}.router")

            if hasattr(router_module, "router"):
                app.include_router(router_module.router)
        except ModuleNotFoundError:
            continue


@app.get("/")
async def root():
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
