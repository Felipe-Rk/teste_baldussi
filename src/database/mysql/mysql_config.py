from unittest.mock import Base
from sqlalchemy import create_engine
from ..mysql.mysql import get_mysql_connection
from mysql.connector import errorcode

from database.mysql import mysql


def setup_mysql_database():
    db_name = "user_db"

    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()

        cursor.execute(f"SHOW DATABASES LIKE '{db_name}';") #verificar se o banco já existe
        result = cursor.fetchone()

        if not result:
            print(f"Banco '{db_name}' não encontrado. Criando...")
            cursor.execute(f"CREATE DATABASE {db_name};")
        else:
            print(f"Banco '{db_name}'. Conectando...")

        connection.database = db_name




        # Verifica se a tabela `users` existe
        cursor.execute("SHOW TABLES LIKE 'users';")
        table_exists = cursor.fetchone()

        if not table_exists:
            print("Tabela 'users' não encontrada. Criando...")

            # Usa o SQLAlchemy para criar a tabela com base no modelo `User`
            engine = create_engine(f'mysql+mysqlconnector://root:root@localhost:3306/{db_name}')
            Base.metadata.create_all(engine)
            print("Tabela 'users' criada com sucesso.")
        else:
            print("Tabela 'users' encontrada.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de autenticação: Verifique usuário/senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erro: Banco de dados não encontrado ou inválido.")
        else:
            print(err)
        return None
    finally:
        cursor.close()
        # connection.close()

    return connection
