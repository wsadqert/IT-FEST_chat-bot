import webbrowser
from aiogram import executor
from rich.traceback import install
import asyncio

from constants import *
from bot import *
from vk_parser import *
import database as db

install(show_locals=True, width=300)
init_table()

print(f'{GREEN}[+] bot started!')
executor.start_polling(dp, skip_updates=True)

print(f'{RED}[*] bot stopped!')

# Save (commit) the changes
con.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed, or they will be lost.
con.close()
