from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from .base import Base


class History(Base):  # type: ignore
    __tablename__ = 'histories'

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    request = Column(String)
    published_timestamp = Column(DateTime)
    response_movie_id = Column(Integer, ForeignKey("movies.movie_kp_id"))
