from fastapi import APIRouter

from api.api_v1.endpoints import login, registration, calendar, apartments

api_router = APIRouter()
api_router.include_router(registration.router, tags=["registration"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
api_router.include_router(apartments.router, prefix="/apartments", tags=["apartment"])
