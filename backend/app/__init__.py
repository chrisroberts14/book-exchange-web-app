"""Module that creates the app for importing in other modules."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .main import root_router

app = FastAPI()
app.include_router(root_router, prefix="", tags=["root"])
# books
# listings / exchange requests
# users

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
