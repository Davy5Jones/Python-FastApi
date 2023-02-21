# main.py

from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from pymongo.errors import OperationFailure

from app.db import db
from app.serializers import serializeDict, serializeList

app = FastAPI()
for col in db.list_collection_names():
    db[col].delete_many({})

db["cats"].insert_one(dict({"name": "Simba", "age": 4, "isCute": bool(False)}))
db["cats"].insert_one(dict({"name": "Mitzi", "age": 2, "isCute": bool(False)}))
db["cats"].insert_one(dict({"name": "Pitzi", "age": 3, "isCute": bool(True)}))
db["cats"].insert_one(dict({"name": "Kitzi", "age": 10, "isCute": bool(True)}))

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


@app.get("/")
async def root():
    return {"Hello World"}


@app.get("/collections")
async def getCollections():
    return db.list_collection_names()


@app.get("/collections/{name}")
async def getCollection(name):
    try:
        db.validate_collection(name)
    except OperationFailure:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    return serializeList(db[name].find())


@app.get("/collections/{name}/{id}")
async def getById(name: str, id: str):
    try:
        db.validate_collection(name)
    except OperationFailure:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    try:
        return serializeDict(db[name].find_one({"_id": ObjectId(id)}))
    except TypeError as err:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find {id}"
        )


@app.get("/collections/{name}/count")
async def getCollectionCount(name):
    try:
        db.validate_collection(name)
    except OperationFailure:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    return db[name].count_documents({})


@app.get("/collections/cats/by/age/over")
async def getCatsAgeOver(age: int):
    return serializeList(db['cats'].find({"age": {"$gte": age}}))


@app.get("/collections/cats/by/name")
async def getCatByName(name: str):
    return serializeList(db['cats'].find({"name": name}))


@app.get("/collections/toys/by/price/below")
async def getToysPriceLower(maxPrice: int):
    return serializeList(db['cats'].find({"price": {"$gte": maxPrice}}))


@app.get("/collections/owners/by/cats/over")
async def getOwnersCatsOver(cats: int):
    return serializeList(db['owners'].find({"catsNumber": {"$gte": cats}}))
