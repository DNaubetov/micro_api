from pydantic import BaseModel
from models.pin import Pin, PinControl
import uuid
import time


class AddPlant(BaseModel):
    name: str
    capacity: int  # Объем горшка
    pin_soil: Pin
    pin_pomp: PinControl


class Plant(AddPlant):
    plant_id: uuid.UUID = uuid.uuid4()
    num_p: int | None = None

    def auto_watering(self):
        soil = self.pin_soil.pin_value
        if soil < 15:
            while soil < 35:
                self.pin_pomp.pin_value = True
                # в 1 сек перекачивает 34 мл воды
            self.pin_pomp.pin_value = False

    # async def manual_watering(self, water_lvl: int):
    #     print('\n\n\n\n\n\n')
    #     max_lvl_water = self.capacity/2
    #     if 0 < water_lvl < max_lvl_water:
    #         self.pin_pomp.pin_value = True
    #         print(self.pin_pomp.pin_num, self.pin_pomp.pin_value)
    #         time.sleep(water_lvl/34)
    #         self.pin_pomp.pin_value = False
    #         print(self.pin_pomp.pin_num, self.pin_pomp.pin_value)
    #
    #         return True
    #     elif water_lvl > self.capacity/2:
    #         return (f"Слишком много воды для данного растения, "
    #                 f"максимально допустимый уровень {self.capacity/2}")
