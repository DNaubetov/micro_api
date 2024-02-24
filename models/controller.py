import uuid
from pydantic import BaseModel
from models.plant import Plant, AddPlant


class AddController(BaseModel):
    plants_list: list[Plant]


class Controller(AddController):
    controller_id: uuid.UUID = uuid.uuid4()

    def add_plant(self, data: AddPlant):
        plant = Plant(**data.model_dump())
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
            self.plant_list.remove(plant_to_remove)
            return True
        return False

    def update_plant(self, id_plant: uuid.UUID, new_data: AddPlant):
        existing_plant = self.get_plant(id_plant)

        if existing_plant is not None:
            try:
                existing_plant.update_from_model(new_data.model_dump())
                return existing_plant
            except ValueError as e:
                return str(e)  # Вернем текст ошибки

        return False  # Растение не найдено

    def get_all_pin(self):
        return list(i.pin_pomp for i in self.plants_list) + list(i.pin_soil for i in self.plants_list)

    def get_all_pin_pomp(self):
        return [i.pin_pomp for i in self.plants_list]

    def get_all_pin_soil(self):
        return [i.pin_soil for i in self.plants_list]

    def write_for_pin(self, pin_num, new_data):
        all_pins = self.get_all_pin()
        if all_pins:
            return list(pin.pin_value == new_data for pin in all_pins if pin.pin_num == pin_num)
        return False
