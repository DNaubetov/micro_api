import asyncio
from models.plant import Plants, PlantsUpdate
from beanie import PydanticObjectId
from database.connection import Database

plants_database = Database(Plants)


async def watering_in_id(plant_id: PydanticObjectId, water_lvl: int):
    plant = await plants_database.get(plant_id)
    print('\n\n\n\n\n\n')
    if 0 < water_lvl < plant.capacity / 2:
        await plant.set({"pin_pomp.pin_state": True, "pin_soil.pin_state": True})
        # await plant.set({})
        print(plant.pin_pomp.pin_num, plant.pin_pomp.pin_state)
        print(plant.pin_soil.pin_num, plant.pin_soil.pin_state)

        await asyncio.sleep(water_lvl / 22)
        await plant.set({"pin_pomp.pin_state": False, "pin_soil.pin_state": False})
        print(plant.pin_pomp.pin_num, plant.pin_pomp.pin_state)

    elif water_lvl > plant.capacity / 2:
        print(f"Слишком много воды для данного растения, "
              f"максимально допустимый уровень {plant.capacity / 2}")
