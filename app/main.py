from typing import Union
from fastapi import FastAPI
from .routers import budget

app = FastAPI()
app.include_router(budget.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
