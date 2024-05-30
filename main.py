# main.py
from fastapi import Depends, FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import logging
import os
import uvicorn
from sqlalchemy.orm import Session
from lands.repository import land_crud
import models
from database import engine, get_db
from lands import land_router
from fastapi.middleware.cors import CORSMiddleware

# JPA의 ddl-auto처럼 자동으로 테이블을 생성해주는 설정
# 테이블 변경 관리는 안되기에 변경 관리까지 원한다면 alembic을 설치해 진행하면 된다
models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.include_router(land_router.app) # 얘가 늘어나는거

app.mount("/js", StaticFiles(directory="js"), name="js")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify the exact origins ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/map", response_class=HTMLResponse)
async def read_index():
    logging.debug("Serving index.html")
    with open("index.html", 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)

# @app.get("/locations", response_class=JSONResponse)
# async def get_locations(db: Session = Depends(get_db)):
#     locations = land_crud.get_all_locations_with_address(db, limit=10000)
#     return JSONResponse(content=locations, status_code=200)

# @app.get("/locations", response_class=JSONResponse)
# async def get_locations(page: int = Query(1, alias="page"), page_size: int = Query(100, alias="pageSize"), db: Session = Depends(get_db)):
#     offset = (page - 1) * page_size
#     locations = land_crud.get_paginated_locations_with_address(db, offset=offset, limit=page_size)
#     return JSONResponse(content=locations, status_code=200)

@app.get("/locations", response_class=JSONResponse)
async def get_locations(type: str = Query(None, alias="type"), page: int = Query(1, alias="page"), page_size: int = Query(100, alias="pageSize"), db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    locations = land_crud.get_filtered_locations(db, type=type, offset=offset, limit=page_size)
    return JSONResponse(content=locations, status_code=200)

if __name__ == '__main__':
    logging.debug("Starting Uvicorn")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")