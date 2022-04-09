from aiogram import types, Bot, Dispatcher
from itertools import compress
from constants import HASHTAGS, SUBSCRIBE_TEXT, UNSUBSCRIBE_TEXT, GROUP_IDS, CONTACTS_TEXT, HELP_IMG_PATH
from tokens import TELEGRAM_TOKEN
import database as db

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Create main menu markup
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1: tuple[str, ...] = ("Подписаться", "Отписаться")
buttons2: tuple[str, ...] = ("Список подписок", 'Наши контакты')
markup.add(*buttons1)
markup.add(*buttons2)

markup_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_help.add(['Помощь'])

empty_markup = types.ReplyKeyboardRemove

section: str = 'main'


# Start/help
@dp.message_handler(commands=['start', 'help'])
async def start(message):
	if section == 'main':
		await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}! Для управления используй кнопки \U0001f447", reply_markup=markup)
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
		db.cur.execute(f"UPDATE data SET {hashtag[1:]} = true WHERE user_id = {message.from_user.id}")
	except Exception as e:
		await call.bot.send_message({message.from_user.id}, f'Произошла неизвестная ошибка!\u274c\U0001f937')
		await call.bot.send_message({message.from_user.id}, str(e))
	else:
		await call.bot.send_message({message.from_user.id}, f'Поздравляю!\U0001f389\U0001f38a Ты успешно подписался на обновления группы вк {GROUP_IDS[HASHTAGS.index(hashtag)]} по хэштегу {hashtag}')
""")

	@dp.callback_query_handler(text='help')
	async def answer_help(call: types.CallbackQuery):
		await bot.send_photo(message.from_user.id, HELP_IMG_PATH)


async def unsubscribe(message):
	global section
	section = 'unsubscribe'

	hashtags = list(compress(HASHTAGS, await _subscriptions(message)))

	# Создание markup`а
	markup_hashtags = types.InlineKeyboardMarkup()
	for hashtag in hashtags:
		markup_hashtags.add(types.InlineKeyboardButton(text=hashtag, callback_data=hashtag[1:]))
	markup_hashtags.add(types.InlineKeyboardButton(text='Помощь', callback_data='help'))

	await bot.send_message(message.from_user.id, UNSUBSCRIBE_TEXT, reply_markup=markup_hashtags)

	# создание и привязка функций к кнопкам
	for hashtag in hashtags:
		exec(f"""
@dp.callback_query_handler(text=hashtag[1:])
async def answer{hashtags.index(hashtag) + 10}(call: types.CallbackQuery):
	try:
		db.cur.execute(f"UPDATE data SET {hashtag[1:]} = false WHERE user_id = {message.from_user.id}")
	except Exception as e:
		await call.bot.send_message({message.from_user.id}, f'Произошла неизвестная ошибка!\u274c\U0001f937')
		await call.bot.send_message({message.from_user.id}, str(e))
	else:
		await call.bot.send_message({message.from_user.id}, f'Поздравляю!\U0001f389\U0001f38a Ты успешно отписался от обновлений группы вк {GROUP_IDS[HASHTAGS.index(hashtag)]} по хэштегу {hashtag}')
""")

	@dp.callback_query_handler(text='help')
	async def answer_help(call: types.CallbackQuery):
		await bot.send_photo(message.from_user.id, HELP_IMG_PATH)
	pass


async def _subscriptions(message):
	# Итерируемся по бд -------------------------------------------------------------------------------------------|||||||||||||||||||||||
	# Выбираем поле с нужным user_id и хештегом ↓                                                                  |||||||||||||||||||||||
	#                        ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                  ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
	return [db.cur.execute(f"SELECT {hashtag[1:]} FROM data WHERE user_id = {message.from_user.id}").fetchone()[0] for hashtag in HASHTAGS]
	# Выбираем 1ую запись (fetchone) и достаём 1ый (и единственный) элемент кортежа -----------------^^^^^^^^^^^^^


async def my_subscriptions(message):
	await bot.send_message(message.from_user.id, 'Ты подписан на хештеги:')
	await bot.send_message(message.from_user.id, '\n'.join(compress(HASHTAGS, await _subscriptions(message))))


@dp.message_handler(content_types=["text"])
async def main(message):
	global section
	if section == 'main':
		txt = message.text.strip()
		if txt == 'Подписаться':
			await subscribe(message)
		elif txt == 'Отписаться':
			await unsubscribe(message)
		elif txt == 'Список подписок':
			await my_subscriptions(message)
		elif txt == 'Управление ботом':
			await start(message)
		elif txt == 'Наши контакты':
			await bot.send_message(message.from_user.id, CONTACTS_TEXT)

	section = 'main'

	# тут сделать бесконечный цикл, вставить парсер
	# while True:
	#   pass
	# pass
