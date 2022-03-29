import telebot
from typing import Final

info: str = """"""
token: Final[str] = "5285755435:AAGkUYDMlugF5J0ksNxBB20ZxNbtnLBs_eY"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(m, res=False):
	bot.send_message(m.chat.id, "Привет! Я на связи! Вот что я умею:")
	bot.send_message(m.chat.id, info)
	bot.send_message(m.chat.id, "Для управления используй кнопки 👇")

