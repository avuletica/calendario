from typing import Optional, List

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Apartment
from schemas import ApartmentCreate


class CRUDApartment(CRUDBase[Apartment, ApartmentCreate]):
    def get_by_name(
        self, db: Session, owner_id: int, apartment_name: str
    ) -> Optional[Apartment]:
        return (
            db.query(self.model)
            .filter(Apartment.owner_id == owner_id, Apartment.name == apartment_name)
            .first()
        )

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, offset: int = 0, limit: int = 100
    ) -> List[Apartment]:
        return (
            db.query(self.model)
            .filter(Apartment.owner_id == owner_id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: ApartmentCreate) -> Apartment:
        db_obj = Apartment(
            owner_id=obj_in.owner_id,
            name=obj_in.name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


apartment = CRUDApartment(Apartment)
