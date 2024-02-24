from pydantic import BaseModel


class AddPinData(BaseModel):
    pin_value: bool | str | None


class Pin(AddPinData):
    pin_num: int
    pin_type: str


