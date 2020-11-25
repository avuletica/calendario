from typing import Optional

from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from models.user import User
from schemas.user import UserCreate


class CRUDUser(CRUDBase[User, UserCreate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user_ = self.get_by_email(db, email=email)
        if not user_:
            return None
        if not verify_password(password, user_.hashed_password):
            return None
        return user_

    @staticmethod
    def is_active(user_: User) -> bool:
        return user_.is_active


user = CRUDUser(User)
