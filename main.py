import uuid

import uvicorn
from fastapi import FastAPI
from utilets.add_data import esp32
from utilets.ip import get_local_ip
from models.pin import Pin, AddPinData
from models.plant import Plant, AddPlant
from routes.get_all import get_all
from routes.get_one import get_one
from fastapi.responses import FileResponse


app = FastAPI(title="Soil system")
app.include_router(get_all)
app.include_router(get_one)

# uvicorn main:app --host 192.168.137.215 --port 8000 --reload

status_soil = False


@app.get("/", response_class=FileResponse)
def root():
    return "template/index.html"


@app.post('/status/{status}')
def post_data(status: bool) -> bool:
    global status_soil
    status_soil = status
    return status_soil


@app.get("/api/v2/get/status/soil/{controller_id}")
def get_status_soil(controller_id: int) -> bool:
    return status_soil


@app.post('/app')
def post_data(data: AddPlant) -> AddPlant:
    return data


@app.post("/api/v2/write/{controller_id}/{pin_num}")
def write_pin(controller_id: int, pin_num: int, data: AddPinData) -> bool:
    return esp32.write_for_pin(pin_num, data.pin_value)


@app.post("/api/v2/add/plant")
def add_new_plant(data: AddPlant) -> dict:
    return {'status': esp32.add_plant(data),
            'id': esp32.plants_list[-1]}


@app.put("/api/v2/up")
def plant_update(id_plant: uuid.UUID, data: AddPlant):
    return esp32.update_plant(id_plant, data)


if __name__ == "__main__":
    if get_local_ip():
        uvicorn.run("main:app", host=get_local_ip(), port=8000, reload=True, workers=3)
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)
