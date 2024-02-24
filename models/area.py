import uuid
from controller import Controller, AddController
from pydantic import BaseModel


class AddArea(BaseModel):
    controllers_list: list[Controller]


class Area(AddArea):
    area_id: uuid.UUID = uuid.uuid4()

    def add_controller(self, data: AddController):
        controller = Controller(**data.model_dump())
        return self.plants_list.append(controller)
