from itertools import compress
from time import sleep
from typing import Literal

from aiogram import types
from aiogram.types import InputFile
from bot import dp, bot
from src.constants import HELP_IMG_PATH, HASHTAGS, OWNER_IDS
from database import cur

# Create main menu markup_main
markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1: tuple[str, ...] = ("Подписаться", "Отписаться", "Список подписок")
buttons2: tuple[str, ...] = ("Помощь", "Контакты для связи", "О разработчике")
markup_main.add(*buttons1)
markup_main.add(*buttons2)

markup_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_help.add(('Помощь', ))


def create_inline_markup(lst: list[str], suffix: str = Literal['s', 'u']) -> types.InlineKeyboardMarkup:
	markup = types.InlineKeyboardMarkup()
	for hashtag in lst:
		markup.add(types.InlineKeyboardButton(text=hashtag, callback_data=hashtag[1:] + suffix))
	markup.add(types.InlineKeyboardButton(text='Помощь', callback_data='help'))
	return markup


@dp.callback_query_handler(text='help')
async def send_help(message):
	await bot.send_photo(message.from_user.id, InputFile(HELP_IMG_PATH))


def _subscriptions(message) -> list[str]:
	# Итерируемся по бд;
	# Выбираем поле с нужным user_id и хештегом;
	# Выбираем 1ую запись (fetchone) и достаём 1ый (и единственный) элемент кортежа;
	try:
		return [cur.execute(f"SELECT {hashtag[1:]} FROM data WHERE user_id = {message.from_user.id}").fetchone()[0] for hashtag in HASHTAGS]
	except TypeError:
		return []


def parser(message):
	hs = compress(HASHTAGS, _subscriptions(message))
	owners = compress(OWNER_IDS, _subscriptions(message))
	while True:
		print('привет)')
		sleep(2 * 3600)
	pass
