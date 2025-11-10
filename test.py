from utils.db_utils import insert_client

insert_client(
    name="João Barreto",
    phone="(12) 99999-9999",
    address="Rua das Ferramentas, 123",
    email="joao@example.com"
)

print("Cliente inserido com sucesso!")