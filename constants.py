from typing import Final
from colorama import Fore
from aiogram import Bot, Dispatcher
from typing import Union
from os import PathLike

PATH: type = Union[str, bytes, PathLike[str], PathLike[bytes]]

# Bot
token: Final[str] = "5285755435:AAGkUYDMlugF5J0ksNxBB20ZxNbtnLBs_eY"
bot = Bot(token=token)
dp = Dispatcher(bot)

info_text: Final[str] = """*здесь будет инфа про скиллы моего бота*"""
contacts_text: Final[str] = """Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты:
Группа ВКонтакте Научим.online https://vk.com/nauchim.online
Сайт с мероприятиями https://www.научим.online"""
subscribe_text: Final[str] = "Выбери канал, на который ты хочешь подписаться:"
hashtags: Final[list[str]] = ["#TechnoCom", "#IT_fest_2022", "#IASF2022", "#ФестивальОКК", "#Нейрофест", "#НевидимыйМир", "#КонкурсНИР", "#VRARFest3D"]

# Database
db_path: PATH = 'data.db'

# Misc
GREEN: Final[str] = Fore.GREEN
RED: Final[str] = Fore.RED
RESET: Final[str] = Fore.RESET
