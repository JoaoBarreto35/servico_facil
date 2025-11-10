from utils.db_utils import connect_db

conn = connect_db()
print("Conexão estabelecida com sucesso!")
conn.close()