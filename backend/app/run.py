import uvicorn

from config import settings


def init():
    uvicorn.run(
        "main:application",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    init()
