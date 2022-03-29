from colorama import Fore
from bot import *
from vk_parser import *
from database import *

GREEN: str = Fore.GREEN
RED: str = Fore.RED
RESET: str = Fore.RESET

print(f'{GREEN}[+] bot started!')
bot.polling(none_stop=True, interval=0)

print(f'{RED}[*] bot stopped!')
