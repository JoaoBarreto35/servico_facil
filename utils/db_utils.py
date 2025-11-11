import sqlite3
import os

def connect_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../db/servico_facil.db")
    conn = sqlite3.connect(db_path)
    return conn



#CRUD Clients
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

def update_client(client_id, name, phone, address, email):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clients
        SET name = ?, phone = ?, address = ?, email = ?
        WHERE id = ?
    """, (name, phone, address, email, client_id))

    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))

    conn.commit()
    conn.close()


#CRUD Service items

def insert_item(name, price, notes):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO service_items (name, price, notes)
        VALUES (?, ?, ?)
    """, (name, price, notes))

    conn.commit()
    conn.close()

def get_all_items():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, price, notes FROM service_items")
    items = cursor.fetchall()

    conn.close()
    return items

def update_item(item_id, name, price, notes):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE service_items
        SET name = ?, price = ?, notes = ?
        WHERE id = ?
    """, (name, price, notes, item_id))

    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM service_items WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()


#CRUD Orders
def insert_order(client_id, date, status, fulfillment_method, notes, completion_date=None):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO orders (client_id, date, status, fulfillment_method, notes, completion_date)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, (client_id, date, status, fulfillment_method, notes, completion_date))

    order_id = cursor.lastrowid  # 🔥 IMPORTANTE: pegar o ID da ordem inserida

    conn.commit()
    conn.close()
    return order_id  # 🔥 RETORNAR o ID

def get_all_orders():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, client_id, date, status, fulfillment_method, notes, completion_date
        FROM orders
    """)
    orders = cursor.fetchall()

    conn.close()
    return orders

def update_order(order_id, client_id, date, status, fulfillment_method, notes, completion_date=None):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET client_id = ?, date = ?, status = ?, fulfillment_method = ?, notes = ?, completion_date = ?
        WHERE id = ?
    """, (client_id, date, status, fulfillment_method, notes, completion_date, order_id))

    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))

    conn.commit()
    conn.close()


#CRUD Order_items
def insert_order_item(order_id, item_id, quantity, unit_price):
    conn = connect_db()
    cursor = conn.cursor()

    print(f"INSERT: order_id={order_id}, item_id={item_id}, quantity={quantity}, unit_price={unit_price}")  # Debug

    cursor.execute("""
        INSERT INTO order_items (order_id, item_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    """, (order_id, item_id, quantity, unit_price))

    conn.commit()
    conn.close()
    print("Item inserido com sucesso!")  # Debug


def get_order_items(order_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT id, item_id, quantity, unit_price
                   FROM order_items
                   WHERE order_id = ?
                   """, (order_id,))

    items = cursor.fetchall()

    # Debug: verificar o que está sendo retornado
    print(f"=== GET_ORDER_ITEMS para ordem {order_id} ===")
    for item in items:
        print(f"ID: {item[0]}, Item_ID: {item[1]}, Qtd: {item[2]}, Preço: {item[3]}")

    conn.close()
    return items

def update_order_item(item_id, quantity, unit_price):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE order_items
        SET quantity = ?, unit_price = ?
        WHERE id = ?
    """, (quantity, unit_price, item_id))

    conn.commit()
    conn.close()

def delete_order_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM order_items WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()


#CRUD accounts
def insert_account(name, amount, due_date, recurring, paid):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO accounts (name, amount, due_date, recurring, paid)
        VALUES (?, ?, ?, ?, ?)
    """, (name, amount, due_date, recurring, paid))

    conn.commit()
    conn.close()

def get_all_accounts():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, amount, due_date, recurring, paid
        FROM accounts
    """)
    accounts = cursor.fetchall()

    conn.close()
    return accounts

def update_account(account_id, name, amount, due_date, recurring, paid):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE accounts
        SET name = ?, amount = ?, due_date = ?, recurring = ?, paid = ?
        WHERE id = ?
    """, (name, amount, due_date, recurring, paid, account_id))

    conn.commit()
    conn.close()

def delete_account(account_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))

    conn.commit()
    conn.close()