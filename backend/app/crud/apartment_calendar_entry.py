from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import ApartmentCalendarEntry
from schemas import ApartmentCalendarEntryCreate


class CRUDApartmentCalendarEntry(
    CRUDBase[ApartmentCalendarEntry, ApartmentCalendarEntryCreate]
):
    def get_multi_by_calendar_id(
        self,
        db: Session,
        *,
        apartment_calendar_ids: List[int],
        datetime_from: datetime = None,
        datetime_to: datetime = None
    ) -> List[ApartmentCalendarEntry]:
        query = db.query(self.model).filter(
            ApartmentCalendarEntry.apartment_calendar_id.in_(apartment_calendar_ids)
        )
        if datetime_from:
            query = query.filter(ApartmentCalendarEntry.start_datetime >= datetime_from)
        if datetime_to:
            query = query.filter(ApartmentCalendarEntry.end_datetime < datetime_to)
        return query.all()

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

    def map_calendar_entries(self, apartment_entries, calendar_entries):
        for entry in calendar_entries:
            data = {
                "start_datetime": entry.start_datetime,
                "end_datetime": entry.end_datetime,
            }
            apartment_entries[str(entry.calendar.apartment_id)].append(data)

        return apartment_entries


apartment_calendar_entry = CRUDApartmentCalendarEntry(ApartmentCalendarEntry)
