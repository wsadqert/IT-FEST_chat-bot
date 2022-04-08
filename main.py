from aiogram import executor
from rich.traceback import install

from constants import *
import bot
import database as db

install(show_locals=True, width=300)
db.init_table()

print(f'{GREEN}[+] bot started!')
executor.start_polling(bot.dp, skip_updates=True)

print(f'{RED}[*] bot stopped!')

# Save (commit) the changes
db.con.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed, or they will be lost.
db.con.close()
