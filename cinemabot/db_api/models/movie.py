from sqlalchemy import Column, Integer, String

from .base import Base


class Movie(Base):  # type: ignore
    __tablename__ = 'movies'

    movie_kp_id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
