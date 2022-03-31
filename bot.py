from aiogram import Bot, Dispatcher, types
from messages import *

__all__ = ['bot', 'dp']

# Init
token: Final[str] = "5285755435:AAGkUYDMlugF5J0ksNxBB20ZxNbtnLBs_eY"
bot = Bot(token=token)
dp = Dispatcher(bot)

# Create main menu markup
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1: tuple[str, ...] = ("Подписаться", "Список подписок")
buttons2: tuple[str, ...] = ('Управление ботом', 'Наши контакты')
markup.add(*buttons1)
markup.add(*buttons2)


# Start/help
@dp.message_handler(commands=['start', 'help'])
async def start(message, res=False):
	await bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Вот что я умею:")
	await bot.send_message(message.chat.id, info)
	await bot.send_message(message.chat.id, "Для управления используй кнопки \U0001f447", reply_markup=markup)


async def subscribe(message):
	pass


async def unsubscribe(message):
	pass


async def my_subscriptions(message):
	pass


@dp.message_handler(content_types=["text"])
async def handle_text(message):
	if message.text.strip() == 'Подписаться':
		await subscribe(message)
	elif message.text.strip() == 'Мои подписки':
		await my_subscriptions(message)
	elif message.text.strip() == 'Управление ботом':
		await start(message)
	elif message.text.strip() == 'Наши контакты':
		await bot.send_message(message.chat.id, contacts)
