from sqlalchemy import Integer, Column
from .base import Base


class User(Base):  # type: ignore
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
