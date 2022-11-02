from .api import Api
from .movie import Movie
import os
import typing as tp


class OmdbApi(Api):
    url = "https://www.omdbapi.com"

    def get_api_params(self, movie_name):
        key = os.environ["OMDB_TOKEN"]
        headers = {}
        page = 1
        params = {"apikey": key, "s": movie_name, "page": page}
        return self.url, params, headers

    def proceed_response(self, req: tp.Optional[dict]) -> tp.Optional[Movie]:
        if req is None:
            return None

        if 'Search' not in req.keys():
            return None

        if not req['Search']:
            return None

        return Movie(req['Search'][0], 'OMDB')
