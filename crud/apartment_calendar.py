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
    def get_by_id(
        self, db: Session, apartment_calendar_id: int
    ) -> Optional[ApartmentCalendar]:
        return (
            db.query(self.model)
            .filter(ApartmentCalendar.id == apartment_calendar_id)
            .first()
        )

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
            file=obj_in.file,
            import_url=obj_in.import_url,
            apartment_id=obj_in.apartment_id,
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
        ret_val = {"entries": [], "file": file}

        for component in calendar.walk():
            data = {}
            if component.name == "VEVENT":
                data["summary"] = component.get("summary")
                data["start_datetime"] = component.get("dtstart").dt
                data["end_datetime"] = component.get("dtend").dt
                if not isinstance(data["start_datetime"], datetime):
                    data["start_datetime"] = datetime.combine(
                        data["start_datetime"], datetime.min.time()
                    )
                if not isinstance(data["end_datetime"], datetime):
                    data["end_datetime"] = datetime.combine(
                        data["end_datetime"], datetime.min.time()
                    )
                ret_val["entries"].append(data)

        ret_val["apartment_name"] = calendar.get("PRODID")
        return ret_val


apartment_calendar = CRUDApartmentCalendar(ApartmentCalendar)
