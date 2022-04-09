from aiogram import types, Bot, Dispatcher
from constants import INFO_TEXT, HASHTAGS, SUBSCRIBE_TEXT, GROUP_IDS, CONTACTS_TEXT
from tokens import TELEGRAM_TOKEN
import database as db

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Create main menu markup
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1: tuple[str, ...] = ("Подписаться", "Список подписок")
buttons2: tuple[str, ...] = ('Управление ботом', 'Наши контакты')
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
		await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}! Вот что я умею:")
		await bot.send_message(message.from_user.id, INFO_TEXT)
		await bot.send_message(message.from_user.id, "Для управления используй кнопки \U0001f447", reply_markup=markup)

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

	# создание и привязка функций к кнопкам
	for hashtag in HASHTAGS:
		# мне пришлось юзать `exec`; у меня не было выхода(((
		# простите пж(
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
		await bot.send_photo(message.from_user.id, 'hashtags.png')


async def unsubscribe(message):
	pass


async def my_subscriptions(message):
	for hashtag in HASHTAGS:
		db.cur.execute(f"SELECT {hash}").fetchall()
		pass
	pass


@dp.message_handler(content_types=["text"])
async def main(message):
	global section
	if section == 'main':
		txt = message.text.strip()
		if txt == 'Подписаться':
			await subscribe(message)
		elif txt == 'Мои подписки':
			await my_subscriptions(message)
		elif txt == 'Управление ботом':
			await start(message)
		elif txt == 'Наши контакты':
			await bot.send_message(message.from_user.id, CONTACTS_TEXT)

	section = 'main'

	# тут сделать бесконечный цикл, вставить парсер
	# while True:
	#	pass
	# pass
