import sqlite3
import os

def connect_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../db/servico_facil.db")
    conn = sqlite3.connect(db_path)
    return conn