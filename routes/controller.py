from typing import List
from beanie import PydanticObjectId
from database.connection import Database
from fastapi import APIRouter, HTTPException, status
from models.controller import Controllers, ControllersUpdate

controllers_router = APIRouter(
    tags=["Controllers"]
)

controllers_database = Database(Controllers)


@controllers_router.get("/", response_model=List[Controllers])
async def retrieve_all_controllers() -> List[Controllers]:
    controllers = await controllers_database.get_all()
    return controllers


@controllers_router.get("{id}/pin/soil", response_model=List[Controllers])
async def get_all_controllers_soil_pin() -> List[Controllers]:
    controllers = await controllers_database.get_all()
    return controllers

@controllers_router.get("/{id}", response_model=Controllers)
async def retrieve_controller(id: PydanticObjectId) -> Controllers:
    controller = await controllers_database.get(id)
    if not controller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Controllers with supplied ID does not exist"
        )
    return controller


@controllers_router.post("/new")
async def create_controller(body: Controllers) -> dict:
    await controllers_database.save(body)
    return {
        "message": "Controllers created successfully"
    }


@controllers_router.put("/{id}", response_model=Controllers)
async def update_controller(id: PydanticObjectId, body: ControllersUpdate) -> Controllers:
    updated_controller = await controllers_database.update(id, body)
    if not updated_controller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Controllers with supplied ID does not exist"
        )
    return updated_controller


@controllers_router.delete("/{id}")
async def delete_controller(id: PydanticObjectId) -> dict:
    controller = await controllers_database.delete(id)
    if not controller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Controllers with supplied ID does not exist"
        )
    return {
        "message": "Controllers deleted successfully."
    }


