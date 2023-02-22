from typing import Union, Dict, Type

from pydantic import BaseModel


class CatBaseSchema(BaseModel):
    name: str
    age: int
    isNice: bool


class CatDto(CatBaseSchema):
    id: str


class ToyBaseSchema(BaseModel):
    title: str
    description: str
    price: int


class OwnerBaseSchema(BaseModel):
    email: str
    catsNumber: int


collection_models: Dict[str, Type] = {
    "cats": CatBaseSchema,
    "toys": ToyBaseSchema,
    "owners": OwnerBaseSchema
}

types = Union[tuple(collection_models.values())]
