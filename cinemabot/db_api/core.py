from sqlalchemy import select, func, insert, desc
from .models.base import Session
from .models import User, Movie, History


def add_user(
        user_id: int,
        *,
        session: Session
) -> None:
    if session.execute(select(User).filter_by(user_id=user_id)).first() is None:
        session.execute(insert(User).values(user_id=user_id))
        session.commit()


def add_movie(
        title: str,
        year: int,
        movie_kp_id: int,
        *,
        session: Session
) -> None:
    if session.execute(select(Movie).filter_by(movie_kp_id=movie_kp_id)).first() is None:
        session.execute(insert(Movie).values(title=title, year=year, movie_kp_id=movie_kp_id))
        session.commit()


def add_history(
        user_id: int,
        request: str,
        response_movie_id: int,
        *,
        session: Session
) -> None:
    session.execute(insert(History).values(user_id=user_id, request=request, response_movie_id=response_movie_id))
    session.commit()


def get_history(
        user_id: int,
        *,
        session: Session
) -> list[tuple]:
    user_history = select(History.request).where(History.user_id == user_id)\
        .order_by(desc(History.published_timestamp))
    return session.execute(user_history).fetchall()


def get_stats(
        user_id: int,
        *,
        session: Session
) -> list[tuple]:
    user_stats = select(Movie.title, Movie.year, func.count(History.user_id).label("cnt")).\
        where(History.user_id == user_id).join(Movie, History.response_movie_id == Movie.movie_kp_id)\
        .group_by(Movie.movie_kp_id).order_by(desc("cnt"))
    return session.execute(user_stats).fetchall()
