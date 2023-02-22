# main.py
from typing import Union

from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from app.db import db
from app.serializers import serializeDict, serializeList

app = FastAPI()
for col in db.list_collection_names():
    db[col].delete_many({})

db["cats"].insert_one(dict({"name": "Simba", "age": 4, "isCute": bool(False)}))
db["cats"].insert_one(dict({"name": "Mitzi", "age": 2, "isCute": bool(False)}))
db["cats"].insert_one(dict({"name": "Pitzi", "age": 3, "isCute": bool(True)}))
db["cats"].insert_one(dict({"name": "Kitzi", "age": 10, "isCute": bool(True)}))
db["cats"].insert_one(dict({"name": "Tommy", "age": 6, "isCute": bool(True)}))

db["toys"].insert_one(dict({"title": "mouse",
                            "description": "a toy mouse",
                            "price": 10}))

db["toys"].insert_one(dict({"title": "scratcher",
                            "description": "scratching post is a wooden post covered in rough material",
                            "price": 40}))

db["toys"].insert_one(dict({"title": "hiding box",
                            "description": "a box with a hole to keep your cat warm",
                            "price": 50}))

db["toys"].insert_one(dict({"title": "rat",
                            "description": "a toy rat your cat can fight",
                            "price": 20}))

db["owners"].insert_one(dict({
    "email": "ido@gmail.com",
    "catsNumber": 5
}))

db["owners"].insert_one(dict({
    "email": "arie@gmail.com",
    "catsNumber": 2
}))

db["owners"].insert_one(dict({
    "email": "kobi@gmail.com",
    "catsNumber": 8
}))


@app.get("/collections")
async def getCollections():
    return {"collections": db.list_collection_names()}


@app.get("/collections/{name}")
async def getCollection(name: str):
    if not bool(db.list_collections(filter={'name': name}).alive):
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    return jsonable_encoder({"items": serializeList(db[name].find())})


@app.get("/collections/{name}/count")
async def getCollectionCount(name: str):
    if not bool(db.list_collections(filter={'name': name}).alive):
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )

    return jsonable_encoder({"count": db[name].count_documents({})})


@app.get("/collections/{name}/fields")
async def getCollectionFields(name: str):
    if not bool(db.list_collections(filter={'name': name}).alive):
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    document = serializeDict(db[name].find_one())
    return {
        "fields": [(field_name, type(field_value).__name__) for field_name, field_value in document.items() if field_name !="_id"]}


@app.get("/collections/{name}/by")
async def getCollection(name: str, field: str, value: Union[int, bool, str]):
    if not bool(db.list_collections(filter={'name': name}).alive):
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    query = {field: {"$exists": True}}

    if db[name].find_one(query) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find field {field}"
        )
    return serializeList(db[name].find({field: value}))


@app.get("/collections/{name}/{id}")
async def getById(name, id):
    if not bool(db.list_collections(filter={'name': name}).alive):
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    try:
        return serializeDict(db[name].find_one({"_id": ObjectId(id)}))
    except TypeError:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find {id} in {name}"
        )

