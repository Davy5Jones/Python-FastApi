from typing import List, Any, Union

from pydantic import BaseModel


class CatBaseSchema(BaseModel):
    name: str
    age: int
    isNice: bool


class ToyBaseSchema(BaseModel):
    title: str
    description: str
    price: int


class OwnerBaseSchema(BaseModel):
    email: str
    catsNumber: int



