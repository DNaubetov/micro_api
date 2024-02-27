import uuid
import uvicorn
from fastapi import FastAPI, Depends
from utilets.add_data import esp32
from utilets.ip import get_local_ip
from models.pin import Pin, AddPinData
from models.plant import Plant, AddPlant
from routes.get_all import get_all
from routes.get_one import get_one
from fastapi.responses import FileResponse

app = FastAPI(title="Soil system", version="2", openapi_tags=[{"name": "post"}])
app.include_router(get_all)
app.include_router(get_one)


# uvicorn main:app --host 192.168.137.215 --port 8000 --reload


@app.get("/", response_class=FileResponse)
async def root():
    return "template/index.html"


@app.post('/api/v2/switch/{status}/{pin_num}', tags=['post'])
async def switch(pin_num: int, status: bool):
    return esp32.switch_status(pin_num, status)


@app.post("/api/v2/write/{controller_id}/{pin_num}", tags=['post'])
async def write_pin(controller_id: int, pin_num: int, data: AddPinData):
    print(data)
    return esp32.write_for_pin(pin_num, data)


@app.post("/api/v2/add/plant", tags=['post'])
async def add_new_plant(data: AddPlant) -> Plant:
    esp32.add_plant(data)
    return esp32.plants_list[-1]


@app.post('/api/v2/manual/{id_plant}/watering', tags=['post'])
async def watering(id_plant: uuid.UUID, water: int) -> bool:
    await esp32.get_plant(id_plant).manual_watering(water_lvl=water)
    return True


@app.put("/api/v2/up")
async def plant_update(id_plant: uuid.UUID, data: AddPlant):
    return esp32.update_plant(id_plant, data)


if __name__ == "__main__":
    if get_local_ip():
        uvicorn.run("main:app", host=get_local_ip(), port=8000, reload=True, workers=3)
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)
