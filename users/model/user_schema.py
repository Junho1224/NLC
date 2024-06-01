

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, EmailStr


class NewUserForm(BaseModel):
    email: str
    name: str
    phone: str
    password: str

    @field_validator('email', 'name', 'phone', 'password', mode='before')
    def check_empty(cls, v):
        if not v or v.isspace():
            raise HTTPException(status_code=422, detail="Empty value is not allowed")
        return v
    
    @field_validator('phone')
    def check_phone(cls, v):
        phone = v.replace("-", "")
        if not v.isdigit():
            raise HTTPException(status_code=422, detail="Phone number should be number")
        return v
    
    @field_validator('password')
    def check_password(cls, v):
        if len(v) < 4:
            raise HTTPException(status_code=422, detail="Password should be longer than 4")
        return v
    

class Token(BaseModel):
    access_token: str
    token_type: str