from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import logging
import os
from requests import Session
import uvicorn

import models
from database import engine, get_db
from lands import land_router

# JPA의 ddl-auto처럼 자동으로 테이블을 생성해주는 설정
# 테이블 변경 관리는 안되기에 변경 관리까지 원한다면 alembic을 설치해 진행하면 된다
models.Base.metadata.create_all(bind=engine) 


logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.include_router(land_router.app)

# 정적 파일 제공
app.mount("/css", StaticFiles(directory="style"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/data", StaticFiles(directory="data"), name="data")


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.post("/lands/")
# def create_land(land: models.Lands, db: Session = Depends(get_db)):
#     db.add(land)
#     db.commit()
#     db.refresh(land)
#     return land


@app.get("/map", response_class=HTMLResponse)
async def read_index():
    logging.debug("Serving index.html")
    with open("index.html", 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/data/locations", response_class=JSONResponse)
async def get_locations():
    logging.debug("Serving locations.json")
    try:
        file_path = os.path.join(os.getcwd(), "data", "locations.json")
        logging.debug(f"Looking for file at: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
            logging.debug(f"Data read from file: {data}")
            locations = json.loads(data)
            return locations
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return JSONResponse(status_code=404, content={"message": "File not found"})
    except Exception as e:
        logging.error(f"Error reading locations.json: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


if __name__ == '__main__':
    logging.debug("Starting Uvicorn")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")