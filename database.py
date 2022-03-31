import sqlite3
con = sqlite3.connect('data.db')
cur = con.cursor()


def init_table():
	try:
		# Create table
		cur.execute('''CREATE TABLE data (user_id int, TechnoCom boolean, IT_fest_2022 boolean, IASF2022 boolean, ФестивальОКК boolean, Нейрофест boolean, НевидимыйМир boolean, КонкурсНИР boolean, VRARFest3D boolean)''')
	except sqlite3.OperationalError:
		# If table `data` already exists, do nothing
		raise


async def init_user(user_id: int):
	# Insert a row of data
	cur.execute(f"INSERT INTO data VALUES ({user_id}, false, false, false, false, false, false, false, false)")
