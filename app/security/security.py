from typing import Optional, MutableMapping, List, Union
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.model.user import User
from sqlalchemy.orm.session import Session
from datetime import datetime, timedelta


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = db.query(User).filter(User.username == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
