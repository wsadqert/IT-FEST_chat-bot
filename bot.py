from aiogram import types, Bot, Dispatcher
from aiogram.types import InputFile
from itertools import compress
from constants import HASHTAGS, SUBSCRIBE_TEXT, UNSUBSCRIBE_TEXT, GROUP_IDS, CONTACTS_TEXT, HELP_IMG_PATH
from tokens import TELEGRAM_TOKEN
import database as db

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Create main menu markup
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1: tuple[str, ...] = ("Подписаться", "Отписаться", "Список подписок")
buttons2: tuple[str, ...] = ("Помощь", "Контакты для связи")
markup.add(*buttons1)
markup.add(*buttons2)

markup_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_help.add(['Помощь'])

empty_markup = types.ReplyKeyboardRemove

section: str = 'main'


@dp.callback_query_handler(text='help')
async def send_help(message):
	await bot.send_photo(message.from_user.id, InputFile(HELP_IMG_PATH))


# Start/help
@dp.message_handler(commands=['start'])
async def start(message):
	if section == 'main':
		await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}! Для управления используй кнопки \u0001f447", reply_markup=markup)
		db.init_user(message.from_user.id)
	else:
		await bot.send_message(message.from_user.id, "Ошибка: бот уже запущен!")


async def subscribe(message):
	global section
	section = 'subscribe'

	# Создание markup`а
	markup_hashtags = types.InlineKeyboardMarkup()
	for hashtag in HASHTAGS:
		markup_hashtags.add(types.InlineKeyboardButton(text=hashtag, callback_data=hashtag[1:]))
	markup_hashtags.add(types.InlineKeyboardButton(text='Помощь', callback_data='help'))
	await bot.send_message(message.from_user.id, SUBSCRIBE_TEXT, reply_markup=markup_hashtags)

	# создание и привязка функций к кнопкам
	for hashtag in HASHTAGS:
		exec(f"""
@dp.callback_query_handler(text=hashtag[1:])
async def answer{HASHTAGS.index(hashtag)}(call: types.CallbackQuery):
	try:
		if '{section}' != 'subscribe':
			raise Exception('unknown section "{section}"')
		db.cur.execute(f"UPDATE data SET {hashtag[1:]} = true WHERE user_id = {message.from_user.id}")
	except Exception as e:
		await call.bot.send_message({message.from_user.id}, f'Произошла неизвестная ошибка!\u274c\u0001f937')
		await call.bot.send_message({message.from_user.id}, str(e))
	else:
		await call.bot.send_message({message.from_user.id}, f'Поздравляю!\u0001f389\u0001f38a Ты успешно подписался на обновления группы VK {GROUP_IDS[HASHTAGS.index(hashtag)]} по хештегу {hashtag}')
""")


async def unsubscribe(message):
	global section
	section = 'unsubscribe'

	hashtags_enabled = list(compress(HASHTAGS, await _subscriptions(message)))

	# Создание markup`а
	markup_hashtags = types.InlineKeyboardMarkup()
	for hashtag in hashtags_enabled:
		markup_hashtags.add(types.InlineKeyboardButton(text=hashtag, callback_data=hashtag[1:]))
	markup_hashtags.add(types.InlineKeyboardButton(text='Помощь', callback_data='help'))

	await bot.send_message(message.from_user.id, UNSUBSCRIBE_TEXT, reply_markup=markup_hashtags)

	# создание и привязка функций к кнопкам
	for hashtag in hashtags_enabled:
		exec(f"""
@dp.callback_query_handler(text=hashtag[1:])
async def answer{hashtags_enabled.index(hashtag) + 10}(call: types.CallbackQuery):
	try:
		if '{section}' != 'unsubscribe':
			raise Exception('unknown section "{section}"')
			db.cur.execute(f"UPDATE data SET {hashtag[1:]} = false WHERE user_id = {message.from_user.id}")
	except Exception as e:
		await call.bot.send_message({message.from_user.id}, f'Произошла неизвестная ошибка!\u274c\u0001f937')
		await call.bot.send_message({message.from_user.id}, str(e))
	else:
		await call.bot.send_message({message.from_user.id}, f'Ты успешно отписался от обновлений группы VK {GROUP_IDS[HASHTAGS.index(hashtag)]} по хештегу {hashtag}. Если это сделано случайно, ты всегда можешь возобновить подписку.')
""")


async def _subscriptions(message) -> list[str]:
	# Итерируемся по бд -------------------------------------------------------------------------------------------|||||||||||||||||||||||
	# Выбираем поле с нужным user_id и хештегом ↓                                                                  |||||||||||||||||||||||
	#                        ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                  ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
	return [db.cur.execute(f"SELECT {hashtag[1:]} FROM data WHERE user_id = {message.from_user.id}").fetchone()[0] for hashtag in HASHTAGS]
	# Выбираем 1ую запись (fetchone) и достаём 1ый (и единственный) элемент кортежа -----------------^^^^^^^^^^^^^


async def my_subscriptions(message):
	if set(await _subscriptions(message)) == {0}:
		await bot.send_message(message.from_user.id, 'Ты ещё не подписан ни на один хештег\u0001f625. Давай это исправим!')
	await bot.send_message(message.from_user.id, 'Ты подписан на хештеги:')
	await bot.send_message(message.from_user.id, '\n'.join(compress(HASHTAGS, await _subscriptions(message))))


@dp.message_handler(content_types=["text"])
async def main(message):
	global section
	if section != 'main':
		return

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

	section = 'main'

	# тут сделать бесконечный цикл, вставить парсер
	# while True:
	#   pass
	# pass
