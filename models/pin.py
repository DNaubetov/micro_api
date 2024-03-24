from pydantic import BaseModel


class PinDataPost(BaseModel):
    pin_value: str | None = None


class PinControl(BaseModel):
    pin_num: int
    pin_state: bool = False


class PinData(PinControl, PinDataPost):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                    "pin_num": 0,
                    "pin_state": False,
                    "pin_value": None
                }
            }
