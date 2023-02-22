# main.py
from typing import Union

from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from app.db import db
from app.schemes import collection_models, types
from app.serializers import serializeDict, serializeList

app = FastAPI()


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
        "fields": [({"field_name": field_name, "type": type(field_value).__name__}) for field_name, field_value in
                   document.items() if field_name != "_id"]}


@app.get("/collections/{name}/filter/{field}")
async def getCollection(name: str, field: str, value: Union[int, bool, str]):
    if not bool(db.list_collections(filter={'name': name}).alive):
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )

    if db[name].find_one(filter={field: {"$exists": True}}) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find field {field}"
        )
    return serializeList(db[name].find({field: value}))


@app.get("/collections/{name}/{id}")
async def getById(name: str, id: str):
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


@app.post("/collections/{name}")
async def addItem(name: str, model: types):
    if not bool(db.list_collections(filter={'name': name}).alive):
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    if type(model) != collection_models.get(name):
        raise HTTPException(
            status_code=400,
            detail=f"Incorrect data"
        )
    idx = db[name].insert_one(dict(model)).inserted_id
    return serializeDict(db[name].find_one({"_id": ObjectId(idx)}))


@app.put("/collections/{name}/{id}")
async def updateItem(name: str, id: str, model: types):
    if not bool(db.list_collections(filter={'name': name}).alive):
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find collection {name}"
        )
    if type(model) != collection_models.get(name):
        raise HTTPException(
            status_code=400,
            detail=f"Incorrect data"
        )
    item = db[name].find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(model)},return_document=True)
    return serializeDict(item)
