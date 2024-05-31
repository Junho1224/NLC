# main.py
from fastapi import Depends, FastAPI, HTTPException, Request, Query, requests
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

from users import user_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# JPA의 ddl-auto처럼 자동으로 테이블을 생성해주는 설정
# 테이블 변경 관리는 안되기에 변경 관리까지 원한다면 alembic을 설치해 진행하면 된다
models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.include_router(land_router.app) # 얘가 늘어나는거
app.include_router(user_router.app) 

app.mount("/js", StaticFiles(directory="js"), name="js")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify the exact origins ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
favicon_path = 'favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/map", response_class=HTMLResponse)
async def read_index():
    logging.debug("Serving index.html")
    with open("index.html", 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)
    
@app.get("/api/kakao_map")
async def kakao_map_proxy(x: float, y: float):
    kakao_api_key = os.getenv('KAKAO_REST_API_KEY')
    url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    params = {"x": x, "y": y, "input_coord": "WGS84"}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return JSONResponse(content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@app.get("/api/locations", response_class=JSONResponse)
async def get_locations(type: str = Query(None, alias="type"), page: int = Query(1, alias="page"), page_size: int = Query(500, alias="pageSize"), db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    locations = land_crud.get_filtered_locations(db, type=type, offset=offset, limit=page_size)
    return JSONResponse(content=locations, status_code=200)

if __name__ == '__main__':
    logging.debug("Starting Uvicorn")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")