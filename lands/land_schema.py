# fastapi에서는 dto를 스키마라고 한다.

from pydantic import BaseModel


class LandsBase(BaseModel):
    atclNo : int
    atclNm: str
    rletTpNm: str
    prc: int
    lat: float
    lng: float

class LandsCreate1   (BaseModel):
    atclNm: str
    rletTpNm: str
    prc: int

class LandsCreate(LandsBase):
    atclNm: str
    rletTpNm: str
    prc: int

class LandsUpdate(LandsBase):
    pass