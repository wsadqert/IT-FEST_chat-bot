from threading import Thread
from itertools import compress

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from src.constants import HASHTAGS, SUBSCRIBE_TEXT, UNSUBSCRIBE_TEXT, GROUP_IDS, CONTACTS_TEXT, ABOUT_TEXT, OWNER_IDS
from src.tokens import TELEGRAM_TOKEN
import database as db
from vk_parser import last_post

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
from bot_additional import create_inline_markup, markup_main, send_help, _subscriptions, parser  # I can`t move it to top of file because of cyclic import

flag = False


# Start/help
@dp.message_handler(commands=['start'])
async def start(message: Message):
	if not db.cur.execute(f"SELECT rowid FROM data WHERE user_id = {message.from_user.id}").fetchall():
		await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}! Для управления используй кнопки \U0001f447", reply_markup=markup_main)
		db.init_user(message.from_user.id)
	else:
		await bot.send_message(message.from_user.id, "Ошибка: бот уже запущен!", reply_markup=markup_main)


async def subscribe(message: Message):
	hashtags_enabled: list[str] = list(compress(HASHTAGS, _subscriptions(message)))
	hashtags2subscr: list[str] = list(set(HASHTAGS) - set(hashtags_enabled))

	# Создание markup`а и отправка сообщения
	await bot.send_message(message.from_user.id, SUBSCRIBE_TEXT, reply_markup=create_inline_markup(hashtags2subscr, 's'))

	# создание и привязка функций к кнопкам
	for hashtag in hashtags2subscr:
		exec(f"""
@dp.callback_query_handler(text='{hashtag[1:]}' + 's')
async def answer{hashtags2subscr.index(hashtag)}(call):
	try:
		db.cur.execute(f"UPDATE data SET {hashtag[1:]} = true WHERE user_id = {message.from_user.id}")
		db.cur.execute(f"UPDATE posts SET {hashtag[1:]} = {last_post(OWNER_IDS[HASHTAGS.index(hashtag)])['id']} WHERE user_id = {message.from_user.id}")
	except Exception as e:
		await call.bot.send_message({message.from_user.id}, f'Произошла неизвестная ошибка!\u274c\U0001f937')
		await call.bot.send_message({message.from_user.id}, str(e))
	else:
		await call.bot.send_message({message.from_user.id}, f'Поздравляю!\U0001f389\U0001f38a Ты успешно подписался на обновления группы VK {GROUP_IDS[HASHTAGS.index(hashtag)]} по хештегу {hashtag}')
""")


async def unsubscribe(message: Message):

	hashtags_enabled = list(compress(HASHTAGS, _subscriptions(message)))
	if not hashtags_enabled:
		await my_subscriptions(message)
		return

	# Создание markup`а и отправка сообщения
	await bot.send_message(message.from_user.id, UNSUBSCRIBE_TEXT, reply_markup=create_inline_markup(hashtags_enabled, 'u'))

	# создание и привязка функций к кнопкам
	for hashtag in hashtags_enabled:
		exec(f"""
@dp.callback_query_handler(text='{hashtag[1:]}' + 'u')
async def answer{hashtags_enabled.index(hashtag) + 10}(call):
	try:
		db.cur.execute(f"UPDATE data SET {hashtag[1:]} = false WHERE user_id = {message.from_user.id}")
	except Exception as e:
		await call.bot.send_message({message.from_user.id}, f'Произошла неизвестная ошибка!\u274c\U0001f937')
		await call.bot.send_message({message.from_user.id}, str(e))
	else:
		await call.bot.send_message({message.from_user.id}, f'Ты успешно отписался от обновлений группы VK {GROUP_IDS[HASHTAGS.index(hashtag)]} по хештегу {hashtag}. Если это сделано случайно, ты всегда можешь возобновить подписку.')
""")


async def my_subscriptions(message: Message):
	if set(_subscriptions(message)) == {0} or not set(_subscriptions(message)):
		await bot.send_message(message.from_user.id, 'Ты ещё не подписан ни на один хештег\U0001f625. Давай это исправим!')
		return
	await bot.send_message(message.from_user.id, 'Ты подписан на хештеги:')
	await bot.send_message(message.from_user.id, '\n'.join(compress(HASHTAGS, _subscriptions(message))))


@dp.message_handler(content_types=["text"])
async def main(message: Message):
	global flag

	txt = message.text.strip()
	match txt:
		case 'Подписаться':
			await subscribe(message)
		case 'Отписаться':
			await unsubscribe(message)
		case 'Список подписок':
			await my_subscriptions(message)
		case "Помощь":
			await send_help(message)
		case "Контакты для связи":
			await bot.send_message(message.from_user.id, CONTACTS_TEXT)
		case "О разработчике":
			await bot.send_message(message.from_user.id, ABOUT_TEXT)

	if not flag:
		th = Thread(target=parser, args=(message,))
		th.start()
	
	flag = True
