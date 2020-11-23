from fastapi import APIRouter

router = APIRouter()


@router.post("/registration")
def registration():
    return {"message": "Registration complete!"}
