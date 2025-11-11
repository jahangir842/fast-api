from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.get("/")
def home():
    return  {"message": "Hello FastAPI!"}

@app.get("/greet/{name}")
def greet(name: str, age: int = 25):
    return {"message": f"Hello, {name}! You are {age} years old."}

