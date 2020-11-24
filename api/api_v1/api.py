from fastapi import APIRouter

from api.api_v1.endpoints import login, registration

api_router = APIRouter()
api_router.include_router(registration.router, tags=["registration"])
api_router.include_router(login.router, tags=["login"])
