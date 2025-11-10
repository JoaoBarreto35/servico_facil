from utils.db_utils import get_all_clients

clients = get_all_clients()

for client in clients:
    print(f"ID: {client[0]} | Name: {client[1]} | Phone: {client[2]}")