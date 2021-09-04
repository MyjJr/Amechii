from sqlalchemy.orm import Session
from typing import Optional

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db_session: Session, *, obj_in: UserCreate) -> User:
        if not obj_in.display_name:
            obj_in.display_name = obj_in.name

        db_obj = User(
            name=obj_in.name,
            display_name=obj_in.display_name,
            icon=obj_in.icon,
            password=get_password_hash(obj_in.password)
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def get_by_name(self, db_session: Session, *, name: str) -> Optional[User]:
        return db_session.query(User).filter(User.name == name).first()

    def authenticate(
        self, db_session: Session,
        *,
        username: str,
        password: str
    ) -> Optional[User]:  # yapf: disable

        user = self.get_by_name(db_session, name=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


user = CRUDUser(User)
