"""Module creating the app."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.users import users
from backend.app.api.books import books


app = FastAPI()
app.include_router(users, prefix="/users", tags=["users"])
app.include_router(books, prefix="/books", tags=["books"])

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root_redirect():
    """
    Redirect to the docs.

    :return:
    """
    return RedirectResponse(url="/docs")
