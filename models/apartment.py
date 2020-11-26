from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from db.base_class import Base


class Apartment(Base):
    __table_args__ = (UniqueConstraint("id", "name", name="unique_id_name"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    owner_id = Column(Integer, ForeignKey("user.id"))

    # Relationship (one-to-one) #
    calendar = relationship("ApartmentCalendar", backref="apartment", uselist=False)
