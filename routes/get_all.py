from fastapi import APIRouter
from models.plant import Plant
from models.pin import Pin, PinControl
from utilets.add_data import esp32

get_all = APIRouter(prefix="/api/v2/get/all", tags=["get All"])


@get_all.get("/plant")
async def get_all_plant() -> list[Plant]:
    return esp32.plants_list


@get_all.get("/pin/soil")
async def pin_soil() -> list[Pin]:
    return esp32.get_all_pin_soil()


@get_all.get("/pin/pomp")
async def pin_pomp() -> list[PinControl]:
    print(esp32.get_all_pin_pomp()[1])
    return esp32.get_all_pin_pomp()


@get_all.get("/soil/status/{controller_id}")
async def humidity_monitoring_pin_status(controller_id: int) -> dict:
    return {i.pin_num: i.pin_state for i in esp32.get_all_pin_soil()}

