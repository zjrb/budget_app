from fastapi import APIRouter, Depends, HTTPException 
from app.db.session import SessionLocal
from pydantic import BaseModel
from app.model.user import User as user_model
from app.model.authtoken import authtoken as authtoken_model
from app.security.security import authenticate, get_password_hash
import uuid
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

class User(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str


@router.post("/create_user")
def create_user(user: User) -> User:

    usr = user.dict()
    usr["password"] = get_password_hash(usr['password'])
    db = SessionLocal.session_factory()

    if db.query(user_model).filter(user_model.username == usr['username']).first() is not None:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = user_model(**usr)

    db.add(new_user)
    db.commit()
    return usr

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal.session_factory()
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = uuid.uuid4()
    db.update(authtoken_model).where(authtoken_model.user_id == user.id).values(token=token)
    return {"access_token": token, "token_type": "bearer"}





    