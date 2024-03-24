from typing import List, Any, Dict
from beanie import PydanticObjectId
from database.connection import Database
from fastapi import APIRouter
from models.controller import Controllers
from models.plant import Plants
from models.pin import PinData, PinControl, PinDataPost

pin_router = APIRouter(
    prefix="/api/pin",
    tags=["Pin"]
)

plants_database = Database(Plants)
controllers_database = Database(Controllers)


@pin_router.get("/all/{controller_id}", response_model=List[Any], summary="Вызов всех пинов")
async def get_all_pin(controller_id: PydanticObjectId) -> List[Any]:
    plants = await plants_database.all_plant_for_controller(controller_id)
    return ([pin.pin_soil for pin in plants] +
            [pin.pin_pomp for pin in plants])


@pin_router.get("/all/soil/{controller_id}", response_model=List[Any], summary="Вызов всех пинов влажности")
async def get_all_soil_pin(controller_id: PydanticObjectId) -> List[Any]:
    plants = await plants_database.all_plant_for_controller(controller_id)
    return [pin.pin_soil for pin in plants]


@pin_router.get("/all/pomp/{controller_id}", response_model=List[Any], summary="Вызов всех пинов помпы")
async def get_all_pomp_pin(controller_id: PydanticObjectId) -> List[Any]:
    plants = await plants_database.all_plant_for_controller(controller_id)
    return [pin.pin_pomp for pin in plants]


@pin_router.get("/all/soil/status/{controller_id}",
                response_model=Dict[Any, Any],
                summary="Вызов состояния всех пинов влажности")
async def get_all_soil_pin_status(controller_id: PydanticObjectId) -> Dict[Any, Any]:
    plants = await plants_database.all_plant_for_controller(controller_id)
    return {pin.pin_soil.pin_num: pin.pin_soil.pin_state for pin in plants}


@pin_router.put("/all/soil/{controller_id}",
                response_model=Plants,
                summary="Изменение данных пина влажности")
async def write_pin_soil(controller_id: PydanticObjectId, data: PinData) -> Plants:
    plant = await Plants.find_one(Plants.pin_soil.pin_num == data.pin_num,
                                  Plants.controller == controller_id)
    return await plant.set({"pin_soil": data})


@pin_router.put("/all/pomp/{controller_id}",
                response_model=Plants,
                summary="Изменение данных пина помпы")
async def write_pin_soil(controller_id: PydanticObjectId, data: PinControl) -> Plants:
    plant = await Plants.find_one(Plants.pin_pomp.pin_num == data.pin_num,
                                  Plants.controller == controller_id)
    return await plant.set({"pin_pomp": data})
