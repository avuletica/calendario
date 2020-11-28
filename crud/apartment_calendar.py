from datetime import datetime, date
from typing import Optional

import aiohttp as aiohttp
from icalendar import Calendar
from pydantic import HttpUrl
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

    def get_by_id(self, db: Session, calendar_id: int) -> Optional[ApartmentCalendar]:
        return db.query(self.model).filter(ApartmentCalendar.id == calendar_id).first()

    def create(
        self, db: Session, *, obj_in: ApartmentCalendarCreate
    ) -> ApartmentCalendar:
        db_obj = ApartmentCalendar(
            summary=obj_in.summary,
            start_datetime=obj_in.start_datetime,
            end_datetime=obj_in.end_datetime,
            apartment_id=obj_in.apartment_id,
            ics_file=obj_in.ics_file,
            import_url=obj_in.import_url,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def fetch_icalendar_from_url(url: HttpUrl):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.read()

    @staticmethod
    def parse_icalendar(file: bytes):
        calendar = Calendar.from_ical(file)
        ret_val = {"ics_file": file}

        for component in calendar.walk():
            if component.name == "VEVENT":
                ret_val["summary"] = component.get("summary")
                ret_val["start_datetime"] = component.get("dtstart").dt
                ret_val["end_datetime"] = component.get("dtend").dt
                if isinstance(ret_val["start_datetime"], date):
                    ret_val["start_datetime"] = datetime.combine(
                        ret_val["start_datetime"], datetime.min.time()
                    )
                if isinstance(ret_val["end_datetime"], date):
                    ret_val["end_datetime"] = datetime.combine(
                        ret_val["end_datetime"], datetime.min.time()
                    )

        ret_val["apartment_name"] = calendar.get("PRODID")
        return ret_val


apartment_calendar = CRUDApartmentCalendar(ApartmentCalendar)
