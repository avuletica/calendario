from db.init_db import init_db
from db.session import SessionLocal


def init_data() -> None:
    db = SessionLocal()
    init_db(db)


init_data()
