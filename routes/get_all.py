from fastapi import APIRouter
from models.plant import Plant
from models.pin import Pin
from utilets.add_data import esp32

get_all = APIRouter(prefix="/api/v2/get/all", tags=["get All"])


@get_all.get("/plant")
def get_all_plant() -> list[Plant]:
    return esp32.plants_list


@get_all.get("/pin")
def pin() -> list[Pin]:
    return esp32.get_all_pin()


@get_all.get("/soil")
def pin_soil() -> list[Pin]:
    return esp32.get_all_pin_soil()


@get_all.get("/pomp")
def pin_pomp() -> list[Pin]:
    return esp32.get_all_pin_pomp()
