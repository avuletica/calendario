import uvicorn

from config import settings


def init():
    uvicorn.run(
        "calendario.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        reload_dirs=["calendario"],
    )


if __name__ == "__main__":
    init()
