from telebot import TeleBot, types
from telebot.types import KeyboardButton
from typing import Final

info: str = """*здесь будет инфа про скиллы моего бота*"""
token: Final[str] = "5285755435:AAGkUYDMlugF5J0ksNxBB20ZxNbtnLBs_eY"
bot: TeleBot = TeleBot(token)

contacts: Final[str] = """Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты:
Группа ВКонтакте Научим.online https://vk.com/nauchim.online
Сайт с мероприятиями https://www.научим.online"""


@bot.message_handler(commands=['start'])
def start(m, res=False):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(KeyboardButton("Факт"))
	markup.add(KeyboardButton("Наши контакты"))

	bot.send_message(m.chat.id, "Привет! Я на связи! Вот что я умею:")
	bot.send_message(m.chat.id, info)
	bot.send_message(m.chat.id, "Для управления используй кнопки 👇")


@bot.message_handler(content_types=["text"])
def handle_text(message):
	if message.text.strip() == 'Наши контакты':
		bot.send_message(message.chat.id, contacts)
