from pydantic import BaseModel


class ColorBase(BaseModel):
    color_name: str
    color_hexa: str
