from telebot import TeleBot, types
from telebot.types import KeyboardButton
from messages import *

token: Final[str] = "5285755435:AAGkUYDMlugF5J0ksNxBB20ZxNbtnLBs_eY"
bot: TeleBot = TeleBot(token)


@bot.message_handler(commands=['start'])
def start(m, res=False):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	buttons = ["привет", "ещё раз привет"]
	markup.add(*buttons)

	bot.send_message(m.chat.id, "Привет! Я на связи! Вот что я умею:")
	bot.send_message(m.chat.id, info)
	bot.send_message(m.chat.id, "Для управления используй кнопки 👇", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
	if message.text.strip() == 'Наши контакты':
		bot.send_message(message.chat.id, contacts)
