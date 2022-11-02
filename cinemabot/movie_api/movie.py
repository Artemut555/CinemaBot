import typing as tp
from .google_link.glink import get_glink


class Movie:
    genres: list[str] = []
    countries: list[str] = []
    title: str = ""
    poster_url: str = ""
    description: str = ""
    art_type: str = ""
    film_length: str = ""
    link: str = ""
    year: tp.Optional[int] = None
    rating: tp.Optional[int] = None
    kp_id: tp.Optional[int] = None

    def __init__(self, movie_dict: dict[str, tp.Any], api: str):
        if api == "OMDB":
            self.title = movie_dict.get("Title", "")
            self.art_type = movie_dict.get("Type", "")
            self.year = movie_dict.get("Year", None)
            self.poster_url = movie_dict.get("Poster", "")
        elif api == "KP":
            self.title = movie_dict.get("nameEn", "")
            self.title = movie_dict.get("nameRu", "")
            self.art_type = movie_dict.get("type", "")
            self.year = movie_dict.get("year", None)
            self.description = movie_dict.get("description", "")
            self.film_length = movie_dict.get("filmLength", "")
            self.countries = [country['country'] for country in movie_dict.get("countries", [])]
            self.genres = [genres['genre'] for genres in movie_dict.get("genres", [])]
            self.rating = movie_dict.get("rating", None)
            self.poster_url = movie_dict.get("posterUrl", "")
            self.kp_id = movie_dict.get("filmId", None)
            self.link = "https://www.kinopoisk.ru/film/" + str(movie_dict.get("filmId", ""))
        else:
            assert "Wrong api name"

    def generate_info(self) -> str:
        title = f"<b>{self.title} ({self.year})</b>\n\n"
        description = f"{self.description}\n\n"
        length = f"Длительность: {self.film_length}\n"
        countries = f"Страны: {', '.join(self.countries)}\n"
        genres = f"Жанры: {', '.join(self.genres)}\n"
        rating = f"Рейтинг: {self.rating}\n"
        link = f"\nИнформация здесь {self.link}\n"

        glink = get_glink(f"{self.title} ({self.year})", self.art_type == "FILM")
        glink_row = f"Смотреть {glink}\n"

        info = "".join([title, description, countries, genres, length, rating, link, glink_row])
        return info
