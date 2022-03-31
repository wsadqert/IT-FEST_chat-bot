import sqlite3
con = sqlite3.connect('data.db')
cur = con.cursor()

try:
	# Create table
	cur.execute('''CREATE TABLE data (int user_id, boolean TechnoCom, boolean IT-fest_2022, boolean IASF2022, boolean ФестивальОКК, boolean Нейрофест, boolean НевидимыйМир, boolean КонкурсНИР, boolean VRARFest3D)''')
except sqlite3.OperationalError:
	pass

# Insert a row of data
cur.execute("INSERT INTO data VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed, or they will be lost.
con.close()
