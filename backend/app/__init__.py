"""Module that creates the app for importing in other modules."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .main import root_router
from .books import book_router
from .listings import listings_router
from .users import user_router

app = FastAPI()
app.include_router(root_router, prefix="", tags=["root"])
app.include_router(book_router, prefix="/books", tags=["books"])
app.include_router(listings_router, prefix="/listings", tags=["listings"])
app.include_router(user_router, prefix="/users", tags=["users"])

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
