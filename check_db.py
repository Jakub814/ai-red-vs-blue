import sqlite3

conn = sqlite3.connect("db/simulation.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM simulation_results")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()