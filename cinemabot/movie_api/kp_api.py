from .api import Api
from .movie import Movie
import os
import typing as tp


class KpApi(Api):
    url = "https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword"

    def get_api_params(self, movie_name: str) -> tuple[str, dict, dict]:
        token = os.environ["KP_TOKEN"]
        headers = {"X-API-KEY": token}
        params = {"keyword": movie_name}
        return self.url, params, headers

    def proceed_response(self, req: tp.Optional[dict]) -> tp.Optional[Movie]:
        if req is None:
            return None

        if 'films' not in req.keys():
            return None

        if not req['films']:
            return None

        return Movie(req['films'][0], "KP")
