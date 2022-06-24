import sqlite3
from time import sleep


print("[!] Iniciando...")

sleep(0.3)

conn = sqlite3.connect('.\config\mysql.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuario (
    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(40) NOT NULL,
    SENHA VARCHAR(40) NOT NULL

);
""")

print('[ OK ] Banco de Dados')