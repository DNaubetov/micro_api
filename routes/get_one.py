import uuid

from fastapi import APIRouter
from models.plant import Plant
from utilets.add_data import esp32

get_one = APIRouter(prefix="/api/v2/get", tags=["get One"])


@get_one.get("/plant/{id_plant}")
async def get_one_plant(id_plant: uuid.UUID) -> Plant | str:
    return esp32.get_plant(id_plant)

