from fastapi import APIRouter

from api.api_v1.endpoints import login, registration, apartment_calendar, apartments, public

api_router = APIRouter()
api_router.include_router(registration.router, tags=["registration"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(apartment_calendar.router, prefix="/apartment-calendar", tags=["apartment-calendar"])
api_router.include_router(apartments.router, prefix="/apartments", tags=["apartment"])
api_router.include_router(public.router, prefix="/public", tags=["public"])
