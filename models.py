from sqlalchemy import Column, Integer, String, VARCHAR, DateTime, Float
from datetime import datetime

from database import Base 

class Lands(Base):
    __tablename__ = 'lands'

    id = Column(Integer, primary_key=True, index=True)
    atclNo = Column(Integer)
    atclNm = Column(VARCHAR(100), nullable=False)
    rletTpNm = Column(VARCHAR(30), nullable=False)
    prc = Column(Integer, nullable=False)
    lat = Column(Float)
    lng = Column(Float)