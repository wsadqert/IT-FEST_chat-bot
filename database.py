import sqlite3
from src.constants import DB_PATH

con = sqlite3.connect(DB_PATH)
cur = con.cursor()


def init_table() -> None:
	try:
		# Create table
		cur.execute('''CREATE TABLE data (user_id int, TechnoCom boolean, IT_fest_2022 boolean, IASF2022 boolean, ФестивальОКК boolean, Нейрофест boolean, НевидимыйМир boolean, КонкурсНИР boolean, VRARFest3D boolean)''')
		cur.execute('''CREATE TABLE posts (user_id int, TechnoCom int, IT_fest_2022 int, IASF2022 int, ФестивальОКК int, Нейрофест int, НевидимыйМир int, КонкурсНИР int, VRARFest3D int)''')
	except sqlite3.OperationalError:
		# If table `data` already exists, do nothing
		pass


def init_user(user_id: int) -> None:
	# Insert a row of data
	if cur.execute(f"SELECT rowid FROM data WHERE user_id = {user_id}").fetchall():
		return
	cur.execute(f"INSERT INTO data VALUES ({user_id}, false, false, false, false, false, false, false, false)")
	cur.execute(f"INSERT INTO posts VALUES ({user_id}, 0, 0, 0, 0, 0, 0, 0, 0)")
