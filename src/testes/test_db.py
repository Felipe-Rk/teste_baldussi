from src.database.mysql.mysql_config import setup_mysql_database
from src.database.mongo.mongo_config import setup_mongo_database


def test_mongo_connection():
    try:
        db = setup_mongo_database()
        print("Conexão com MongoDB realizada com sucesso!")
        print(f"Banco conectado: {db.name}")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")

if __name__ == "__main__":
    test_mongo_connection()


def test_mysql_connection():
    try:
        connection = setup_mysql_database()
        if connection:
            print("Conexão com MySQL realizada com sucesso!")
            print(f"Banco conectado: {connection.database}")
    except Exception as e:
        print(f"Erro ao conectar ao MySQL: {e}")

if __name__ == "__main__":
    test_mysql_connection()





