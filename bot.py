from aiogram import Bot, Dispatcher, types
from constants import *
from database import *

all__ = ['bot', 'dp']

# Create main menu markup
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1: tuple[str, ...] = ("Подписаться", "Список подписок")
buttons2: tuple[str, ...] = ('Управление ботом', 'Наши контакты')
markup.add(*buttons1)
markup.add(*buttons2)

section: str = 'main'


# Start/help
@dp.message_handler(commands=['start', 'help'])
async def start(message, res=False):
	user_id = message.from_user.id
	await bot.send_message(user_id, f"Привет, {message.from_user.first_name}! Вот что я умею:")
	await bot.send_message(user_id, info_text)
	await bot.send_message(user_id, "Для управления используй кнопки \U0001f447", reply_markup=markup)

	try:
		init_user(user_id)
	except:
		raise


async def subscribe(message):
	global section
	section = 'subscribe'

	async def help(message):
		if message.text.strip() == "Помощь":
			await bot.send_photo(message.from_user.id, 'hashtags.png')

	markup_hashtags = types.InlineKeyboardMarkup()
	for hashtag in hashtags:
		markup_hashtags.add(types.InlineKeyboardButton(text=hashtag, callback_data=hashtag[1:]))

	await bot.send_message(message.from_user.id, subscribe_text, reply_markup=markup_hashtags)

	for hashtag in hashtags:
		@dp.callback_query_handler(text=hashtag[1:])
		async def answer(call: types.CallbackQuery):
			print('answering...')
			try:
				cur.execute(f"UPDATE data SET {hashtag[1:]} = true WHERE user_id = {message.from_user.id}")
			except:
				await call.bot.send_message(message.from_user.id, f'Произошла неизвестная ошибка!\u274c\U0001f937')
			else:
				await call.bot.send_message(message.from_user.id, f'Поздравляю!\U0001f389\U0001f38a Вы успешно подписались на обновления группы вк по хэштегу {hashtag}')


async def unsubscribe(message):
	pass


async def my_subscriptions(message):
	pass


@dp.message_handler(content_types=["text"])
async def main(message):
	if section == 'main':
		if message.text.strip() == 'Подписаться':
			await subscribe(message)
		elif message.text.strip() == 'Мои подписки':
			await my_subscriptions(message)
		elif message.text.strip() == 'Управление ботом':
			await start(message)
		elif message.text.strip() == 'Наши контакты':
			await bot.send_message(message.chat.id, contacts_text)
