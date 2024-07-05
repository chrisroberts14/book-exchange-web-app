"""Root end points for the API."""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse


root_router = APIRouter()


@root_router.get("/")
async def docs_redirect():
    """
    Redirects to the API documentation.

    :return:
    """
    return RedirectResponse(url="/docs")
