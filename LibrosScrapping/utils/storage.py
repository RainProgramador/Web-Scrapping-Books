import sqlite3
import os

DB_PATH = os.path.join("data", "libros.db")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS libros (
                    id INTEGER PRIMARY KEY,
                    titulo TEXT,
                    enlace TEXT
                )''')
    conn.commit()
    conn.close()

def guardar_libro(titulo, enlace):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO libros (titulo, enlace) VALUES (?, ?)", (titulo, enlace))
    conn.commit()
    conn.close()
