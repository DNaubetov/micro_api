from pydantic import BaseModel
from models.pin import Pin
import uuid
import time


class AddPlant(BaseModel):
    name: str
    capacity: int  # Объем горшка
    pin_soil: Pin
    pin_pomp: Pin


class Plant(AddPlant):
    plant_id: uuid.UUID = uuid.uuid4()

    def update_from_model(self, model_data: dict):
        for field, value in model_data.items():
            setattr(self, field, value)

    def auto_watering(self):
        soil = self.pin_soil.pin_value
        if soil < 15:
            while soil < 35:
                self.pin_pomp.pin_value = True
                # в 1 сек перекачивает 34 мл воды
            self.pin_pomp.pin_value = False

    def manual_watering(self, water_lvl: int):
        max_lvl_water = self.capacity/2
        if 0 < water_lvl < max_lvl_water:
            self.pin_pomp.pin_value = True
            time.sleep(water_lvl/34)
            self.pin_pomp.pin_value = False
            return True
        elif water_lvl > self.capacity/2:
            return (f"Слишком много воды для данного растения, "
                    f"максимально допустимый уровень {self.capacity/2}")
