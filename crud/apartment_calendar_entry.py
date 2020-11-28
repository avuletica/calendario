from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import ApartmentCalendarEntry
from schemas import ApartmentCalendarEntryCreate


class CRUDApartmentCalendarEntry(
    CRUDBase[ApartmentCalendarEntry, ApartmentCalendarEntryCreate]
):
    def create(
        self, db: Session, *, obj_in: ApartmentCalendarEntryCreate
    ) -> ApartmentCalendarEntry:
        db_obj = ApartmentCalendarEntry(
            summary=obj_in.summary,
            start_datetime=obj_in.start_datetime,
            end_datetime=obj_in.end_datetime,
            apartment_calendar_id=obj_in.apartment_calendar_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


apartment_calendar_entry = CRUDApartmentCalendarEntry(ApartmentCalendarEntry)
