# model.py

from sqlalchemy import Column, Integer, String, VARCHAR, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(50), nullable=False)
    password = Column(VARCHAR(50), nullable=False)
    phone = Column(VARCHAR(50), nullable=False)
    date = Column(DateTime, default=datetime.now)
    del_yn = Column(VARCHAR(1), default='Y')


class Lands(Base):
    __tablename__ = 'lands'

    id = Column(Integer, primary_key=True, index=True)
    area = Column(Integer, nullable=False) # 생각해보니 가지고있을 필요 없음.
    atclNo = Column(Integer) # 네이버 번호
    atclNm = Column(VARCHAR(100), nullable=False) #아파트/상가 명
    rletTpNm = Column(VARCHAR(30), nullable=False) #상가 구분
    tradTpNm = Column(VARCHAR(30)) #"매매/전세/월세 구분",
    flrInfo = Column(String(30)) #"층수(물건층/전체층)",
    prc = Column(Integer, nullable=False) # 가격
    rentPrc = Column(Integer) #월세
    hanPrc = Column(String(30)) #"보증금",
    spc1 = Column(String(30)) # "계약면적(m2) -> 평으로 계산 : * 0.3025",
    spc2 = Column(String(30)) # "전용면적(m2) -> 평으로 계산 : * 0.3025", 
    direction = Column(String(30)) # "집 방향",
    atclFetrDesc = Column(String(500)) # "[한줄 정보]",
    tagList = Column(String(500)) # “[”기타 정보”]”,
    bildNm = Column(String(30)) # "동수",
    
    # Relationship with LandsAdd
    lands_add = relationship("LandsAdd", back_populates="lands")


class LandsAdd(Base):
    __tablename__ = 'lands_add'

    id = Column(Integer, primary_key=True, index=True)
    area = Column(Integer, ForeignKey('lands.id'), nullable=False)
    lat = Column(Float) # 위도
    lng = Column(Float) # 경도
    road_address = Column(String(100)) #도로명주소
    address = Column(String(100)) # 지번주소

    # Relationship with Lands
    lands = relationship("Lands", back_populates="lands_add")