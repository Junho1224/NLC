

from requests import Session
from models import Users
from users.model.user_schema import NewUserForm

#비밀번호 해시 처리
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(email: str, db: Session):
    return db.query(Users).filter(Users.email == email).first()

def create_user(new_user: NewUserForm, db: Session):
    hashed_pw = pwd_context.hash(new_user.password)
    user =Users (
        email=new_user.email,
        name=new_user.name,
        phone=new_user.phone,
        password=hashed_pw
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)