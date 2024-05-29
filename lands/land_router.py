from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends

from lands import land_schema, land_crud

app = APIRouter(
    prefix="/lands",
    tags=["lands"]
)

@app.post(path="/create")
async def create_land(new_house: land_schema.LandsCreate, db: Session = Depends(get_db)):
    return land_crud.insert_land(new_house, db)

@app.get(path="/read", response_model= land_schema.LandsBase)
async def read_land(db: Session = Depends(get_db)):
    return land_crud.get_all_lands(db)

@app.get(path="/read/{land_id}")
async def read_land(land_id: int, db: Session = Depends(get_db)):
    return land_crud.get_land(land_id, db)