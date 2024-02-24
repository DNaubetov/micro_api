import uuid
from controller import Controller
from pydantic import BaseModel


class AddArea(BaseModel):
    id_area: uuid.UUID = uuid.uuid4()
    controllers_list: list[Controller]
