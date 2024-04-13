import uvicorn
from fastapi import FastAPI
from utilets.add_data import esp32
from utilets.ip import get_local_ip
from database.connection import Settings
from routes.controller import controllers_router
from routes.plant import plants_router
from routes.pin import pin_router
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await settings.initialize_database()
    yield


app = FastAPI(lifespan=lifespan, title="Soil system", version="2",
              openapi_tags=[{"name": "Полив"}])

settings = Settings()


app.include_router(controllers_router, prefix="/controllers")
app.include_router(pin_router, prefix="/pin")
app.include_router(plants_router, prefix="/plants")


# uvicorn main:app --host 192.168.137.215 --port 8000 --reload


@app.get("/", response_class=FileResponse)
async def root():
    return "template/index.html"


if __name__ == "__main__":
    if get_local_ip():
        uvicorn.run("main:app", host=get_local_ip(), port=8010, reload=True, workers=3)
    uvicorn.run("main:app", host='127.0.0.1', port=8000)
