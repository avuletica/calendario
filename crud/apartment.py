from typing import Optional, List

from sqlalchemy.orm import Session

from api.utils.utils import calculate_availability, eliminate_overlaps
from crud.base import CRUDBase
from models import Apartment
from schemas import ApartmentCreate


class CRUDApartment(CRUDBase[Apartment, ApartmentCreate]):
    def get_by_name(
        self, db: Session, owner_id: int, apartment_name: str
    ) -> Optional[Apartment]:
        return (
            db.query(self.model)
            .filter(Apartment.owner_id == owner_id, Apartment.name == apartment_name)
            .first()
        )

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, offset: int = 0, limit: int = 100
    ) -> List[Apartment]:
        return (
            db.query(self.model)
            .filter(Apartment.owner_id == owner_id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: ApartmentCreate) -> Apartment:
        db_obj = Apartment(
            owner_id=obj_in.owner_id,
            name=obj_in.name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def init_cleaning_schedule(self, apartments, apartment_entries):
        cleaning_schedule = {
            item.name: {
                "entries": apartment_entries[str(item.id)],
                "next_cleaning_time": None,
                "availability_range": [],
            }
            for item in apartments
        }
        return cleaning_schedule

    def calculate_availability(self, cleaning_schedule):
        for item in cleaning_schedule.values():
            availability_ranges, next_cleaning_time = calculate_availability(
                item["entries"]
            )
            item["next_cleaning_time"] = next_cleaning_time
            item["availability_range"].extend(availability_ranges)
            del item["entries"]

        return cleaning_schedule

    def calculate_cleaning_schedule(self, cleaning_schedule):
        while any(d.get("availability_range") for d in cleaning_schedule.values()):
            remaining_availability = []
            for key, value in cleaning_schedule.items():
                availability_range = value.get("availability_range")

                if availability_range is None or len(availability_range) == 0:
                    continue

                remaining_availability.append(
                    {
                        "apartment_name": key,
                        "availability_range": availability_range[0],
                    }
                )

            elimination = eliminate_overlaps(*remaining_availability)
            for apartment in elimination["apartments"]:
                cleaning_schedule[apartment]["next_cleaning_time"].append(
                    elimination["next_cleaning_time"]
                )
                cleaning_schedule[apartment]["availability_range"].pop()

                if len(cleaning_schedule[apartment]["availability_range"]) == 0:
                    del cleaning_schedule[apartment]["availability_range"]

        for item in cleaning_schedule.values():
            item["next_cleaning_time"].sort()

        return cleaning_schedule


apartment = CRUDApartment(Apartment)
