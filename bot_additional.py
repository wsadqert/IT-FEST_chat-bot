from itertools import compress
from time import sleep
from aiogram import types
from aiogram.types import InputFile
from bot import dp, bot
from constants import HELP_IMG_PATH, HASHTAGS
from database import cur

# Create main menu markup_main
markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1: tuple[str, ...] = ("Подписаться", "Отписаться", "Список подписок")
buttons2: tuple[str, ...] = ("Помощь", "Контакты для связи")
markup_main.add(*buttons1)
markup_main.add(*buttons2)

markup_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_help.add(('Помощь', ))


def create_inline_markup(lst: list[str]) -> types.InlineKeyboardMarkup:
	markup = types.InlineKeyboardMarkup()
	for hashtag in lst:
		markup.add(types.InlineKeyboardButton(text=hashtag, callback_data=hashtag[1:]))
	markup.add(types.InlineKeyboardButton(text='Помощь', callback_data='help'))
	return markup


@dp.callback_query_handler(text='help')
async def send_help(message):
	await bot.send_photo(message.from_user.id, InputFile(HELP_IMG_PATH))


async def _subscriptions(message) -> list[str]:
	# Итерируемся по бд -------------------------------------------------------------------------------------------|||||||||||||||||||||||
	# Выбираем поле с нужным user_id и хештегом ↓                                                                  |||||||||||||||||||||||
	#                        ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                  ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
	return [cur.execute(f"SELECT {hashtag[1:]} FROM data WHERE user_id = {message.from_user.id}").fetchone()[0] for hashtag in HASHTAGS]
	# Выбираем 1ую запись (fetchone) и достаём 1ый (и единственный) элемент кортежа -----------------^^^^^^^^^^^^^


async def parser(message):
	hs = compress(HASHTAGS, await _subscriptions(message))

	sleep(2 * 3600)
	pass
