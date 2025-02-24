import sqlite3

con = sqlite3.connect('./MasoeroPollicino.db')
cur = con.cursor()

cur.execute("SELECT * FROM UTENTI")
print(cur.fetchall())