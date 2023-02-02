from fastapi import APIRouter, Depends, HTTPException 
from app.db.session import SessionLocal
from pydantic import BaseModel
from app.model.user import User as user_model
from app.model.purchase import Purchase as purchase_model
from app.model.budget import Budget as budget_model
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

class Budget(BaseModel):
    name: str
    start_budget: int


class Purchase(BaseModel):
    item: str
    cost: int   

@router.post("/create_user")
def create_user(user: User) -> User:

    
    usr = user.dict()
    usr["id"] = uuid.uuid4()
    usr["password"] = get_password_hash(usr['password'])
    db = SessionLocal.session_factory()

    if db.query(user_model).filter(user_model.username == usr['username']).first() is not None:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = user_model(**usr)
    new_token = authtoken_model(user_id=new_user.id, token=uuid.uuid4())
    db.add(new_user)
    db.commit()
    db.add(new_token)
    db.commit()
    return usr

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal.session_factory()
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = uuid.uuid4()
  
    db.query(authtoken_model).where(authtoken_model.user_id == user.id).update({"token": token})
    db.commit()
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(auth_token: str):
    db = SessionLocal.session_factory()
    current_user = db.query(user_model).join(authtoken_model).filter(authtoken_model.token == auth_token).first()
    return current_user


@router.post("/create_budget")
def create_budget(budget: Budget, auth_token: str):
    db = SessionLocal.session_factory()
    current_user = db.query(user_model).join(authtoken_model).filter(authtoken_model.token == auth_token).first()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    new_budget = budget_model(name=budget.name, start_budget=budget.start_budget, user_id=current_user.id, curr_budget=budget.start_budget)
    db.add(new_budget)
    db.commit()
    return new_budget

@router.post("/logout")
def logout(auth_token: str):
    db = SessionLocal.session_factory()
    current_user = db.query(user_model).join(authtoken_model).filter(authtoken_model.token == auth_token).first()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    db.query(authtoken_model).where(authtoken_model.user_id == current_user.id).update({"token": None})
    db.commit()
    return "Logged out"




@router.post("/add_purchase")
def add_purchase(purchase: Purchase, auth_token: str):
    db = SessionLocal.session_factory()
    current_user = db.query(user_model).join(authtoken_model).filter(authtoken_model.token == auth_token).first()
    budget = db.query(budget_model).filter(budget_model.user_id == current_user.id).first()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    new_purchase = purchase_model(item=purchase.item, cost=purchase.cost, user_id=current_user.id)
    budget.curr_budget -= purchase.cost
    db.add(new_purchase)
    db.commit()
    return new_purchase



    