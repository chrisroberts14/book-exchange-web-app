"""Module creating the app."""

from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.users import users
from backend.app.api.books import books
from backend.app.api.listings import listings
from backend.app.api.auth import auth, oauth2_scheme, get_current_user


app = FastAPI()
app.include_router(users, prefix="/users", tags=["users"])
app.include_router(
    books, prefix="/books", tags=["books"], dependencies=[Depends(get_current_user)]
)
app.include_router(
    listings,
    prefix="/listings",
    tags=["listings"],
    dependencies=[Depends(oauth2_scheme)],
)
app.include_router(auth, prefix="/auth", tags=["auth"])

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root_redirect() -> RedirectResponse:
    """
    Redirect to the docs.

    :return:
    """
    return RedirectResponse(url="/docs")
