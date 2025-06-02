from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

items_db = {}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI CI/CD Demo"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items/")
async def create_item(item: Item):
    item_id = len(items_db) + 1
    items_db[item_id] = item.dict()
    return {"id": item_id, **items_db[item_id]}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
