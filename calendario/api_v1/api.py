from fastapi import APIRouter

from calendario.api_v1.endpoints import registration
from calendario.api_v1.endpoints import login

api_router = APIRouter()
api_router.include_router(registration.router, tags=["registration"])
api_router.include_router(login.router, tags=["login"])
