import sqlite3
import os

def connect_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../db/servico_facil.db")
    conn = sqlite3.connect(db_path)
    return conn

def insert_client(name, phone, address, email):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clients (name, phone, address, email)
        VALUES (?, ?, ?, ?)
    """, (name, phone, address, email))

    conn.commit()
    conn.close()

def get_all_clients():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, phone, address, email FROM clients")
    clients = cursor.fetchall()

    conn.close()
    return clients