import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from constants import START_MESSAGE, HELP_MESSAGE, NO_HISTORY, \
    HISTORY_HEADER, NO_STATS, STATS_HEADER, EMPTY_TITLE, NOT_FOUND, TIP_MESSAGE
from db_api.models.base import Session, clear_database
from movie_api.kp_api import KpApi
from db_api.core import get_history, add_history, add_movie, add_user, get_stats


bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)
clear_database()
session = Session()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(START_MESSAGE)


@dp.message_handler(commands=['help'])
async def send_commands(message: types.Message):
    await message.answer(HELP_MESSAGE)


@dp.message_handler(commands=['history'])
async def send_history(message: types.Message):
    history = get_history(message.from_user.id, session=session)
    if not history:
        return await message.answer(NO_HISTORY)

    header = HISTORY_HEADER
    string_repr = "\n".join([hist[0] for hist in reversed(history[-15:])])
    await message.answer(header + string_repr, parse_mode="HTML")


@dp.message_handler(commands=['stats'])
async def send_stats(message: types.Message):
    stats = get_stats(message.from_user.id, session=session)
    if not stats:
        return await message.answer(NO_STATS)

    header = STATS_HEADER
    res = [f"{stat[0]} ({stat[1]}): {stat[2]}" for stat in stats[:15]]
    await message.answer(header + "\n".join(res), parse_mode="HTML")


@dp.message_handler(commands=['movie'])
async def get_movie(message: types.Message):
    mess = message.text.split(maxsplit=1)
    if len(mess) < 2:
        return await message.answer(EMPTY_TITLE)

    movie_name = mess[1]

    api = KpApi()
    movie = await api.get_api_result(movie_name)

    if movie is None:
        return await message.answer(NOT_FOUND)

    user_id = message.from_user.id
    add_user(user_id, session=session)
    add_movie(movie.title, movie.year, movie.kp_id, session=session)
    add_history(user_id, movie_name, movie.kp_id, session=session)

    await bot.send_photo(message.chat.id, types.InputFile.from_url(movie.poster_url))
    await message.answer(movie.generate_info(), parse_mode="HTML")


@dp.message_handler()
async def send_tip(message: types.Message):
    await message.answer(TIP_MESSAGE)


if __name__ == '__main__':
    executor.start_polling(dp)
