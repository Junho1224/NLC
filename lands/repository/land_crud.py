


from requests import Session
from sqlalchemy import or_
from lands.model.land_schema import LandsBase, LandsCreate
from models import Lands, LandsAdd


def get_filtered_locations(db: Session, type: str, offset: int, limit: int):
    query = db.query(Lands, LandsAdd).join(LandsAdd, Lands.area == LandsAdd.area)
    if type:
        type_list = type.split(',')
        query = query.filter(or_(*[Lands.rletTpNm == t for t in type_list]))
    results = query.offset(offset).limit(limit).all()
    
    locations = []
    for land, address in results:
        location = {
            "id": land.id,
            "atclNm": land.atclNm,
            "rletTpNm": land.rletTpNm,
            "tradTpNm" : land.tradTpNm,
            "flrInfo" : land.flrInfo,
            "prc": land.prc,
            "rentPrc": land.rentPrc,
            "hanPrc": land.hanPrc,
            "spc1": land.spc1,
            "spc2": land.spc2,
            "direction": land.direction,
            "atclFetrDesc": land.atclFetrDesc,
            "tagList": land.tagList,
            "bildNm": land.bildNm,
            "lat": address.lat,
            "lng": address.lng,
            "road_address": address.road_address,
            "address": address.address
        }
        locations.append(location)
    
    return locations

def get_paginated_locations_with_address(db: Session, offset: int, limit: int):
    results = db.query(Lands, LandsAdd).join(LandsAdd, Lands.area == LandsAdd.area).offset(offset).limit(limit).all()
    
    locations = []
    for land, address in results:
        location = {
            "id": land.id,
            "atclNm": land.atclNm,
            "rletTpNm": land.rletTpNm,
            "prc": land.prc,
            "lat": address.lat,
            "lng": address.lng,
            "road_address": address.road_address,
            "address": address.address
        }
        locations.append(location)
    
    return locations

def get_all_locations_with_address(db: Session, limit: int):
    results = db.query(Lands, LandsAdd).join(LandsAdd, Lands.area == LandsAdd.area).limit(limit).all()
    
    locations = []
    for land, address in results:
        location = {
            "id": land.id,
            "atclNm": land.atclNm,
            "rletTpNm": land.rletTpNm,
            "prc": land.prc,
            "lat": address.lat,
            "lng": address.lng,
            "road_address": address.road_address,
            "address": address.address
        }
        locations.append(location)
    
    return locations

def get_limited_locations(db: Session, limit: int):
    lands = db.query(Lands).limit(limit).all()
    lands_add = db.query(LandsAdd).limit(limit).all()
    
    locations = []
    for land in lands:
        location = {
            "id": land.id,
            "atclNm": land.atclNm,
        }
        locations.append(location)
    
    for add in lands_add:
        location = {
            "id": add.id,
            "road_address": add.road_address,
            "lat": add.lat,
            "lng": add.lng
        }
        locations.append(location)
    
    return locations


def insert_land(new_house: LandsCreate, db: Session):
    post = Lands(
        atclNm = new_house.atclNm,
        rletTpNm = new_house.rletTpNm,
        prc = new_house.prc
    )
    db.add(post)
    db.commit()

    return post

def get_all_lands(db: Session):
    list = db.query(Lands).all()
    return [LandsBase(atclNm=land.atclNm, rletTpNm=land.rletTpNm, prc=land.prc) for land in list]
   

def get_land(land_id: int, db: Session):
    land = db.query(Lands).filter(Lands.atclNo == land_id).first()
    return LandsBase(atclNm=land.atclNm, rletTpNm=land.rletTpNm, prc=land.prc) if land else None