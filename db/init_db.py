from sqlalchemy.orm import Session

import crud
import schemas


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email="john@doe.com")
    if not user:
        user_in = schemas.UserCreate(
            email="john@doe.com",
            password="password",
        )
        user = crud.user.create(db, obj_in=user_in)

    apartment_name = "apartment_1"
    apartment_1 = crud.apartment.get_by_name(
        db, owner_id=user.id, apartment_name=apartment_name
    )
    if not apartment_1:
        apartment_1 = schemas.ApartmentCreate(
            owner_id=user.id,
            name=apartment_name,
        )
        crud.apartment.create(db, obj_in=apartment_1)

    apartment_name = "apartment_2"
    apartment_2 = crud.apartment.get_by_name(
        db, owner_id=user.id, apartment_name=apartment_name
    )
    if not apartment_2:
        apartment_2 = schemas.ApartmentCreate(
            owner_id=user.id,
            name=apartment_name,
        )
        crud.apartment.create(db, obj_in=apartment_2)

    apartment_name = "apartment_3"
    apartment_3 = crud.apartment.get_by_name(
        db, owner_id=user.id, apartment_name=apartment_name
    )
    if not apartment_3:
        apartment_3 = schemas.ApartmentCreate(
            owner_id=user.id,
            name=apartment_name,
        )
        crud.apartment.create(db, obj_in=apartment_3)
