from colorama import Fore
from aiogram import executor
from rich.traceback import install
import asyncio

from messages import *
from bot import *
from vk_parser import *
from database import *

install(show_locals=True, width=300)

GREEN: str = Fore.GREEN
RED: str = Fore.RED
RESET: str = Fore.RESET

print(f'{GREEN}[+] bot started!')
executor.start_polling(dp, skip_updates=True)

print(f'{RED}[*] bot stopped!')
