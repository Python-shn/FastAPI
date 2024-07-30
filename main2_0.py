from fastapi import FastAPI, Path, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

# inventory = {
#     1: {
#         "name": "Milk",
#         "price": 25,
#         "brand": "Omfed"
#     }
# }
inventory = {}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The Id of the item you'd like to view", gt=0, lt=5)):
    return inventory[item_id]

@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None, test: int):
    for item_id in inventory:
        # if inventory[item_id]["name"] == name:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found." )

@app.get("/")
def home():
    return {"Data":"Hello"}

@app.get("/about")
def about():
    return {"Data":"About"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        # return {"Error": "Item ID already exists."}
        raise HTTPException(status_code=400, detail="Item Id already exists." )
    # inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        # return {"Error": "Item ID does not exists."}
        raise HTTPException(status_code=404, detail="Item Id does not exists." )
    
    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int):
    if item_id not in inventory:
        # return {"Error": "ID does not exist."}
        raise HTTPException(status_code=404, detail="Item Id does not exist." )
    
    del inventory[item_id]
    return {"Success": "Item deleted!"}
