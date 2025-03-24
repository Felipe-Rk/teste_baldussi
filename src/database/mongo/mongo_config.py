# from .mongo import get_mongo_client

# def setup_mongo_database():
#     client = get_mongo_client()
#     db_name = "transcricao_db"

#     if db_name not in client.list_database_names(): #verifica se o banco já existe, se não ele cria um 
#         print(f"Banco '{db_name}' não encontrado. Criando...")
#         db = client[db_name]
#         # db.create_collection("dummy_collection") #coleção somente para iniciar a conexão 
#     else:
#         print(f"Banco '{db_name}'. Conectando...")
#         db = client[db_name]

#     return db


from src.database.mongo.mongo import get_mongo_client

def setup_mongo_database():
    print("🔹 Inicializando conexão única com MongoDB...")

    client = get_mongo_client()
    db_name = "transcricao_db"

    if db_name not in client.list_database_names():
        print(f"⚠️ Banco '{db_name}' não encontrado. Criando...")
        db = client[db_name]
    else:
        print(f"✅ Banco '{db_name}' encontrado.")

    return client[db_name]
