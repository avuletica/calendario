from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from db.base_class import Base


class ApartmentCalendarEntry(Base):
    __tablename__ = "apartment_calendar_entry"

    id = Column(Integer, primary_key=True)
    summary = Column(String(128))
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    apartment_calendar_id = Column(Integer, ForeignKey("apartment_calendar.id"))
