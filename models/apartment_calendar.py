from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    LargeBinary,
    UniqueConstraint,
)

from db.base_class import Base


class ApartmentCalendar(Base):
    __tablename__ = "apartment_calendar"
    __table_args__ = (UniqueConstraint("apartment_id", name="unique_apartment_id"),)

    id = Column(Integer, primary_key=True)
    summary = Column(String(128))
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    ics_file = Column(LargeBinary, nullable=False)
    apartment_id = Column(Integer, ForeignKey("apartment.id"))
