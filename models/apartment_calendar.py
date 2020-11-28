from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from db.base_class import Base


class ApartmentCalendar(Base):
    __tablename__ = "apartment_calendar"
    __table_args__ = (UniqueConstraint("apartment_id", name="unique_apartment_id"),)

    id = Column(Integer, primary_key=True)
    file = Column(LargeBinary, nullable=False)
    import_url = Column(String)
    apartment_id = Column(Integer, ForeignKey("apartment.id"))

    # Relationship (one-to-many) #
    entries = relationship("ApartmentCalendarEntry", backref="calendar")
