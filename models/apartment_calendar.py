from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from db.base_class import Base


class ApartmentCalendar(Base):
    __tablename__ = "apartment_calendar"

    id = Column(Integer, primary_key=True)
    summary = Column(String(128))
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    ics_file = Column(JSONB, nullable=False)
    apartment_id = Column(Integer, ForeignKey("apartment.id"))
