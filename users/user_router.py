from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session
from jose import jwt
from datetime import datetime
from datetime import timedelta

from users.model import user_schema
from users.repository import user_crud
from database import get_db

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


app = APIRouter(
    prefix="/users",
    tags=["users"]
)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/test")
async def test_user():
    return {"message": "This is a user test"}

@app.get("/read")
async def read_user():
    return {"message": "This is a user read"}

@app.post("/signup")
async def signup(new_user: user_schema.NewUserForm, db: Session = Depends(get_db)):
    # 회원 존재 여부 확인
    user = user_crud.get_user(new_user.email, db)

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user_crud.create_user(new_user, db)

    return HTTPException(status_code=status.HTTP_200_OK, detail="User created successfully")

@app.post("/login")
async def login(response: Response, login_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #회원 확인
    user = user_crud.get_user(login_form.username, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    # 로그인
    res = user_crud.verify_password(login_form.password, user.password)

    # 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    if not res:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    # 쿠키에 저장
    response.set_cookie(
        key="access_token",
        value=access_token,
        expires=access_token_expires,
        httponly=True,)
    
    return HTTPException(status_code=status.HTTP_200_OK, detail="Login successful" )

@app.get(path="/logout")
async def logout(response: Response, request: Request):
    access_token = request.cookies.get("access_token")

    # 쿠키 삭제
    response.delete_cookie(key="access_token")

    return HTTPException(status_code=status.HTTP_200_OK, detail="Logout successful")