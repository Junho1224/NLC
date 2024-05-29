


from requests import Session

from lands.land_schema import LandsBase, LandsCreate
from models import Lands


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