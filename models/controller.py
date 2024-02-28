import asyncio
import time
import uuid
from pydantic import BaseModel
from models.pin import Pin, AddPinData
from models.plant import Plant, AddPlant


class AddController(BaseModel):
    plants_list: list[Plant]


class Controller(AddController):
    controller_id: uuid.UUID = uuid.uuid4()

    def add_plant(self, data: AddPlant):
        plant = Plant(plant_id=uuid.uuid4(), **data.model_dump())
        return self.plants_list.append(plant)

    def get_plant(self, id_plant: uuid.UUID):
        res = next((plant for plant in self.plants_list if plant.plant_id == id_plant), None)

        if res:
            return res
        elif res is None:
            return 'Неверный id'

    def remove_plant(self, id_plant: uuid.UUID):
        plant_to_remove = self.get_plant(id_plant)

        if plant_to_remove is not None:
            self.plants_list.remove(plant_to_remove)
            return True, self.plants_list  # Возвращаем True и обновленный список растений
        return False, self.plants_list  # Возвращаем False и текущий список растений

    def update_plant(self, id_plant: uuid.UUID, new_data: AddPlant):
        existing_plant_index = next((i for i, plant in enumerate(self.plants_list) if plant.plant_id == id_plant), None)

        if existing_plant_index is not None:
            existing_plant = self.plants_list[existing_plant_index].copy()

            # Проверка и обновление каждого поля
            if hasattr(new_data, 'name'):
                existing_plant.name = new_data.name
            if hasattr(new_data, 'capacity'):
                existing_plant.capacity = new_data.capacity
            if hasattr(new_data, 'pin_soil'):
                existing_plant.pin_soil = new_data.pin_soil
            if hasattr(new_data, 'pin_pomp'):
                existing_plant.pin_pomp = new_data.pin_pomp

            # Замена объекта в списке
            self.plants_list[existing_plant_index] = existing_plant

            return existing_plant, self.plants_list  # Возвращаем обновленное растение и список растений
        else:
            return None, self.plants_list  # Возвращаем None, если растение не найдено, и текущий список растений

    def get_all_pin(self):
        return list(i.pin_pomp for i in self.plants_list) + list(i.pin_soil for i in self.plants_list)

    def get_all_pin_pomp(self):
        return [i.pin_pomp for i in self.plants_list]

    def get_all_pin_soil(self):
        return [i.pin_soil for i in self.plants_list]

    def write_for_pin(self, pin_num: int, new_data: AddPinData):
        all_pins = self.get_all_pin()
        if all_pins:
            for i in all_pins:
                if i.pin_num == pin_num:
                    i.pin_value = new_data.pin_value
                    return i.pin_value

    def switch_status(self, pin_num: int, new_state: bool):
        all_pins = self.get_all_pin_soil()
        if all_pins:
            for i in all_pins:
                if i.pin_num == pin_num:
                    i.pin_state = new_state
                    return i
        return 'Pin не найден'

    async def watering(self, id_plant: uuid.UUID, water_lvl: int):
        plant = self.get_plant(id_plant)
        print('\n\n\n\n\n\n')
        max_lvl_water = plant.capacity / 2
        if 0 < water_lvl < max_lvl_water:
            self.switch_status(pin_num=plant.pin_soil.pin_num, new_state=True)
            self.write_for_pin(plant.pin_pomp.pin_num, AddPinData(pin_value=True))
            print(plant.pin_pomp.pin_num, plant.pin_pomp.pin_value)
            await asyncio.sleep(water_lvl / 22)
            self.write_for_pin(plant.pin_pomp.pin_num, AddPinData(pin_value=False))
            self.switch_status(pin_num=plant.pin_soil.pin_num, new_state=False)
            print(plant.pin_pomp.pin_num, plant.pin_pomp.pin_value)
            return True

        elif water_lvl > plant.capacity / 2:
            return (f"Слишком много воды для данного растения, "
                    f"максимально допустимый уровень {plant.capacity / 2}")

    def get_plant_in_num(self, plant_num: int):
        res = next((plant for plant in self.plants_list if plant.num_p == plant_num), None)

        if res:
            return res
        elif res is None:
            return 'Неверный id'

    async def watering_in_num(self, num_plant: int, water_lvl: int):
        plant = self.get_plant_in_num(num_plant)
        print('\n\n\n\n\n\n')
        max_lvl_water = plant.capacity / 2
        if 0 < water_lvl < max_lvl_water:
            self.switch_status(pin_num=plant.pin_soil.pin_num, new_state=True)
            self.write_for_pin(plant.pin_pomp.pin_num, AddPinData(pin_value=True))
            print(plant.pin_pomp.pin_num, plant.pin_pomp.pin_value)
            await asyncio.sleep(water_lvl / 22)
            self.write_for_pin(plant.pin_pomp.pin_num, AddPinData(pin_value=False))
            self.switch_status(pin_num=plant.pin_soil.pin_num, new_state=False)
            print(plant.pin_pomp.pin_num, plant.pin_pomp.pin_value)
            return True

        elif water_lvl > plant.capacity / 2:
            return (f"Слишком много воды для данного растения, "
                    f"максимально допустимый уровень {plant.capacity / 2}")
