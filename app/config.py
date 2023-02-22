from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI = "mongodb+srv://Davy:1234@cluster0.suf5rch.mongodb.net/?retryWrites=true&w=majority"
    MONGO_INITDB_DATABASE = "CatProject"


settings = Settings()
