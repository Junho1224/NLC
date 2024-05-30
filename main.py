# main.py
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import logging
import os
import uvicorn
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from lands import land_router, land_crud

# JPA의 ddl-auto처럼 자동으로 테이블을 생성해주는 설정
# 테이블 변경 관리는 안되기에 변경 관리까지 원한다면 alembic을 설치해 진행하면 된다
models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.include_router(land_router.app)

app.mount("/js", StaticFiles(directory="js"), name="js")


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/map", response_class=HTMLResponse)
async def read_index():
    logging.debug("Serving index.html")
    with open("index.html", 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/locations", response_class=JSONResponse)
async def get_locations(db: Session = Depends(get_db)):
    locations = land_crud.get_all_locations_with_address(db, limit=10000)
    return JSONResponse(content=locations, status_code=200)

if __name__ == '__main__':
    logging.debug("Starting Uvicorn")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")