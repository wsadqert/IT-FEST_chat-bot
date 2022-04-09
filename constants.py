from typing import Final
from colorama import Fore
from typing import Union
from os import PathLike

PATH: Final[type] = Union[str, bytes, PathLike[str], PathLike[bytes]]

# Bot
INFO_TEXT: Final[str] = """*здесь будет инфа про скиллы моего бота*"""
CONTACTS_TEXT: Final[str] = """Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты:
Группа ВКонтакте Научим.online https://vk.com/nauchim.online
Сайт с мероприятиями https://www.научим.online"""
SUBSCRIBE_TEXT: Final[str] = "Выбери канал, на который ты хочешь подписаться:"

# Database
DB_PATH: Final[PATH] = './data.db'

# VK
HASHTAGS: Final[list[str]] = [
	"#TechnoCom",
	"#IT_fest_2022",
	"#IASF2022",
	"#ФестивальОКК",
	"#Нейрофест",
	"#НевидимыйМир",
	"#КонкурсНИР",
	"#VRARFest3D"
]
URLS: Final[list[str]] = [
	'https://vk.com/technocom2022',
	'https://vk.com/itfest2022',
	'https://vk.com/aerospaceproject',
	'https://vk.com/okk_fest',
	'https://vk.com/neurofest2022',
	'https://vk.com/nauchim.online',
	'https://vk.com/nauchim.online',
	'https://vk.com/nauchim.online'
]
GROUP_IDS: Final[list[str]] = [
	'technocom2022',
	'itfest2022',
	'aerospaceproject',
	'okk_fest',
	'neurofest2022',
	'nauchim.online',
	'nauchim.online',
	'nauchim.online'
]
OWNER_IDS: Final[list[int]] = [
	-210998761,
	-210985709,
	-196557207,
	-211638918,
	-211803420,
	-200248443,
	-200248443,
	-200248443
]

# Misc
GREEN: Final[str] = Fore.GREEN
RED: Final[str] = Fore.RED
RESET: Final[str] = Fore.RESET
