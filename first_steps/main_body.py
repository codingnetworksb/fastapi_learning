

from fastapi import FastAPI
from models import Item
from typing import Union

app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# Request body + path parameters
@app.put("/items/{item_id}")
async def create_item_p(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# Request body + path + query parameters
@app.put("/items/{item_id}")
async def create_item_q(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
