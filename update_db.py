import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("ALTER TABLE trabajos ADD COLUMN inicio_trabajo DATETIME")
cur.execute("ALTER TABLE trabajos ADD COLUMN fin_trabajo DATETIME")
cur.execute("ALTER TABLE trabajos ADD COLUMN tiempo_total INTEGER")

conn.commit()
conn.close()

print("Base de datos actualizada")
