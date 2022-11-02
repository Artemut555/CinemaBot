from .movie import Movie
import aiohttp
import typing as tp
from abc import ABC, abstractmethod


async def get_response(url: str, params: dict["str", tp.Any], headers: dict[str, tp.Any]) -> tp.Optional[dict]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url, params=params, headers=headers) as resp:
                return await resp.json()
        except aiohttp.InvalidURL:
            return None
        except AssertionError:
            return None


class Api(ABC):
    @abstractmethod
    def get_api_params(self, movie_name: str) -> tuple[str, dict, dict]:
        pass

    @abstractmethod
    def proceed_response(self, req: tp.Optional[dict]):
        pass

    async def get_api_result(self, movie_name: str) -> tp.Optional[Movie]:
        url, params, headers = self.get_api_params(movie_name)
        resp = await get_response(url, params, headers)
        movie = self.proceed_response(resp)
        return movie
