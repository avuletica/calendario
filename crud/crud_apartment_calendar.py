from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import ApartmentCalendar
from schemas import ApartmentCalendarCreate


class CRUDApartmentCalendar(CRUDBase[ApartmentCalendar, ApartmentCalendarCreate]):
    def create(self, db: Session, *, obj_in: ApartmentCalendarCreate) -> ApartmentCalendar:
        db_obj = ApartmentCalendar(
            summary=obj_in.summary,
            start_datetime=obj_in.start_datetime,
            end_datetime=obj_in.end_datetime,
            apartment_id=obj_in.apartment_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


apartment_calendar = CRUDApartmentCalendar(ApartmentCalendar)
