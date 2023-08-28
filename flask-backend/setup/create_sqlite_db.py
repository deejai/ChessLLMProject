from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).parent.parent

conn = sqlite3.connect(ROOT_DIR / "db.sqlite3")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS table1 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER);")
cursor.execute("CREATE TABLE IF NOT EXISTS table2 (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, price REAL);")

cursor.execute("INSERT INTO table1 (name, age) VALUES ('Alice', 30);")
cursor.execute("INSERT INTO table1 (name, age) VALUES ('Bob', 40);")

cursor.execute("INSERT INTO table2 (item, price) VALUES ('Apple', 1.2);")
cursor.execute("INSERT INTO table2 (item, price) VALUES ('Banana', 0.5);")

conn.commit()
conn.close()
