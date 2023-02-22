from app.db import db
from main import app


@app.on_event("startup")
def init():
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
    db["owners"].insert_one(dict({
        "email": "niv@gmail.com",
        "catsNumber": 1
    }))
    db["owners"].insert_one(dict({
        "email": "rotem@gmail.com",
        "catsNumber": 0
    }))
