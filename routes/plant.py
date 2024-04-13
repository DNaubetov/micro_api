from typing import List, Any
from core.watering import watering_in_id
from beanie import PydanticObjectId
from database.connection import Database
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from models.plant import Plants, PlantsUpdate
from models.controller import Controllers

plants_router = APIRouter(
    tags=["Plants"]
)

plants_database = Database(Plants)
controllers_database = Database(Controllers)


@plants_router.get("/", response_model=List[Plants])
async def get_all_plants() -> List[Plants]:
    plants = await plants_database.get_all()
    return plants


@plants_router.get("/controller/{controller_id}", response_model=List[Any])
async def get_all_pin(controller_id: PydanticObjectId) -> List[Any]:
    plants = await plants_database.all_plant_for_controller(controller_id)
    return plants


@plants_router.get("/{id}", response_model=Plants)
async def retrieve_plant(id: PydanticObjectId) -> Plants:
    plant = await plants_database.get(id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant with supplied ID does not exist"
        )
    return plant


@plants_router.post("/new")
async def create_plant(body: Plants) -> dict:
    await plants_database.save(body)

    return {
        "message": "Plants created successfully"
    }


@plants_router.put("/{id}", response_model=Plants)
async def update_plant(id: PydanticObjectId, body: PlantsUpdate) -> Plants:
    updated_plant = await plants_database.update(id, body)
    if not updated_plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plants with supplied ID does not exist"
        )
    return updated_plant


@plants_router.delete("/{id}")
async def delete_plant(id: PydanticObjectId) -> dict:
    plant = await plants_database.delete(id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plants with supplied ID does not exist"
        )
    return {
        "message": "Plants deleted successfully."
    }


@plants_router.post("/watering/{plant_id}", summary="Метод для полива растения")
async def watering_system(id: PydanticObjectId, water: int, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(watering_in_id, id, water)
    return {"message": "Полив запущен"}
