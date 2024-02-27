from pydantic import BaseModel


class AddPinData(BaseModel):
    pin_value: bool | str | None = None


class Pin(AddPinData):
    pin_num: int
    pin_state: bool = False


class PinControl(AddPinData):
    pin_num: int
    pin_value: bool = False
