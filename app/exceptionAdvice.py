from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from main import app


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    body = jsonable_encoder(exc)
    return JSONResponse({"body": body})
