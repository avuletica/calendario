from typing import Optional

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import ApartmentCalendar
from schemas import ApartmentCalendarCreate


class CRUDApartmentCalendar(CRUDBase[ApartmentCalendar, ApartmentCalendarCreate]):
    def get_by_apartment_id(
        self, db: Session, apartment_id: int
    ) -> Optional[ApartmentCalendar]:
        return (
            db.query(self.model)
            .filter(ApartmentCalendar.apartment_id == apartment_id)
            .first()
        )

    def create(
        self, db: Session, *, obj_in: ApartmentCalendarCreate
    ) -> ApartmentCalendar:
        db_obj = ApartmentCalendar(
            summary=obj_in.summary,
            start_datetime=obj_in.start_datetime,
            end_datetime=obj_in.end_datetime,
            apartment_id=obj_in.apartment_id,
            ics_file=obj_in.ics_file,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


apartment_calendar = CRUDApartmentCalendar(ApartmentCalendar)
