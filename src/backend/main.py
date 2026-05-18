import uvicorn
from core.modules import register_routers
from fastapi import FastAPI

app = FastAPI()


register_routers(app)


@app.get("/")
async def root():
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
