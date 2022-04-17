import asyncio
from itertools import compress
from time import sleep
from typing import Literal

from aiogram import types, Bot
from aiogram.types import InputFile, Message

from bot import dp, bot
from src.constants import HELP_IMG_PATH, HASHTAGS, OWNER_IDS
from database import cur
from vk_parser import last_post, post_text

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
async def send_help(message: Message):
	await bot.send_photo(message.from_user.id, InputFile(HELP_IMG_PATH))


def _subscriptions(message: Message) -> list[str]:
	# Итерируемся по бд;
	# Выбираем поле с нужным user_id и хештегом;
	# Выбираем 1ую запись (fetchone) и достаём 1ый (и единственный) элемент кортежа;
	try:
		return [cur.execute(f"SELECT {hashtag[1:]} FROM data WHERE user_id = {message.from_user.id}").fetchone()[0] for hashtag in HASHTAGS]
	except TypeError:
		return []


def parser(message: Message):
	hs: list = list(compress(HASHTAGS, _subscriptions(message)))
	owners: list = list(compress(OWNER_IDS, _subscriptions(message)))
	
	while True:
		for hash_ in hs:
			owner = owners[hs.index(hash_)]
			
			old_id: int = cur.execute(f"SELECT {hash_[1:]} FROM posts WHERE user_id = {message.from_user.id}").fetchone()[0]
			new_id: int = last_post(owner)['id']
			
			if old_id != new_id:
				asyncio.run_coroutine_threadsafe(bot.send_message(message.from_user.id, post_text(last_post(owner))), asyncio.new_event_loop())  # НЕ РАБОТАЕТ
		
		sleep(2 * 3600)
