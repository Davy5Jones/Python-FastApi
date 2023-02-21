import pymongo
from pymongo import MongoClient

from config import settings

client = MongoClient(settings.mongodb_uri)
db = client['CatProject']

Cat = db.cats
Toy = db.toys
Owner = db.owners
Cat.create_index([("name", pymongo.ASCENDING)], unique=True)
Owner.create_index([("email", pymongo.ASCENDING)], unique=True)
Toy.create_index([("title", pymongo.ASCENDING)], unique=True)
