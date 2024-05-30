# model.py

from sqlalchemy import Column, Integer, String, VARCHAR, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Lands(Base):
    __tablename__ = 'lands'

    id = Column(Integer, primary_key=True, index=True)
    area = Column(Integer, nullable=False)
    atclNo = Column(Integer)
    atclNm = Column(VARCHAR(100), nullable=False)
    rletTpNm = Column(VARCHAR(30), nullable=False)
    tradTpNm = Column(VARCHAR(30))
    flrInfo = Column(String(30))
    prc = Column(Integer, nullable=False)
    rentPrc = Column(Integer)
    hanPrc = Column(String(30))
    spc1 = Column(String(30))
    spc2 = Column(String(30))
    direction = Column(String(30))
    atclFetrDesc = Column(String(500))
    tagList = Column(String(500))
    bildNm = Column(String(30))
    lat = Column(Float)
    lng = Column(Float)

    # Relationship with LandsAdd
    lands_add = relationship("LandsAdd", back_populates="lands")


class LandsAdd(Base):
    __tablename__ = 'lands_add'

    id = Column(Integer, primary_key=True, index=True)
    area = Column(Integer, ForeignKey('lands.area'), nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    road_address = Column(String(100))
    address = Column(String(100))

    # Relationship with Lands
    lands = relationship("Lands", back_populates="lands_add")