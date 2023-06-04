"""
Run a Live Server:
# uvicorn main:app --reload

Check API Response:
# http://127.0.0.1:8000/

Interactive API Docs with Swagger UI:
# http://127.0.0.1:8000/docs

Interactive API Docs with ReDoc:
# http://127.0.0.1:8000/redocs

"""

from fastapi import FastAPI
from enum import Enum
from typing import Union  # < Python 3.9


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# Path Parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Path Parameters with Predefined values
#     If you have a path operation that receives a path parameter,
#     but you want the possible valid path parameter values to be predefined,
#     you can use a standard Python Enum.


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# Query Parameters:
#     When you declare other function parameters that are not part of the path parameters,
#     they are automatically interpreted as "query" parameters.
#     http://127.0.0.1:8000/items/?skip=0&limit=10
@app.get("/items/")
async def read_item_q(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# Optional parameters
#    The same way, you can declare optional query parameters, by setting their default to None
@app.get("/items/{item_id}")
async def read_item_o(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Query parameter type conversion:
#    http://127.0.0.1:8000/items/foo?short=1    -> Bool: True
#    http://127.0.0.1:8000/items/foo?short=yes  -> Bool: True
#    http://127.0.0.1:8000/items/foo?short=on   -> Bool: True
#    http://127.0.0.1:8000/items/foo?short=true -> Bool: True
@app.get("/items/{item_id}")
async def read_item_c(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Required query parameters
#    http://127.0.0.1:8000/items_r/test?needy=obligao
@app.get("/items_r/{item_id}")
async def read_user_item_r(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
