from pydantic import BaseModel
from models.pin import PinData, PinControl
import uuid
from beanie import Document, PydanticObjectId


class Plants(Document):
    controller: PydanticObjectId
    num_p: int | None = None
    name: str
    capacity: int  # Объем горшка
    pin_soil: PinData
    pin_pomp: PinControl

    class Config:
        json_schema_extra = {
            "example": {
                "controller": "65ff5cc2e234a03e40276fd7",
                "num_p": 0,
                "name": "Название цветка",
                "capacity": 0,
                "pin_soil": {
                    "pin_num": 0,
                    "pin_state": False,
                    "pin_value": None
                },
                "pin_pomp": {
                    "pin_state": False,
                    "pin_num": 0
                }
            }
        }

    class Settings:
        name = "plants"


class PlantsUpdate(BaseModel):
    controller: PydanticObjectId
    num_p: int | None = None
    name: str
    capacity: int  # Объем горшка
    pin_soil: PinData
    pin_pomp: PinControl

    class Config:
        json_schema_extra = {
            "example": {
                "controller": "65ff5cc2e234a03e40276fd7",
                "num_p": 0,
                "name": "Название цветка",
                "capacity": 0,
                "pin_soil": {
                    "pin_num": 0,
                    "pin_state": False,
                    "pin_value": None
                },
                "pin_pomp": {
                    "pin_state": False,
                    "pin_num": 0
                }
            }
        }


class AddPlant(BaseModel):
    num_p: int | None = None
    name: str
    capacity: int  # Объем горшка
    pin_soil: PinData
    pin_pomp: PinControl


class Plant(AddPlant):
    plant_id: uuid.UUID = uuid.uuid4()

    def auto_watering(self):
        soil = self.pin_soil.pin_state
        if soil < 15:
            while soil < 35:
                self.pin_pomp.pin_state = True
                # в 1 сек перекачивает 34 мл воды
            self.pin_pomp.pin_state = False
