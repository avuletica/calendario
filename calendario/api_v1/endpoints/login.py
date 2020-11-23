from fastapi import APIRouter

router = APIRouter()


@router.post("/registration")
def login():
    return {"token": "JWT TOKEN"}


