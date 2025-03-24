# import time
# from unittest.mock import Base
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from ..mysql.mysql import get_mysql_connection
# from mysql.connector import errorcode

# from database.mysql import mysql

# Base = declarative_base()

# def setup_mysql_database():
#     print("🔹 Iniciando servidor MySQL...")

#     db_name = "user_db"
#     restart_needed = False  

#     try:
#         print("🔹 Verificando dados...")

#         connection = get_mysql_connection()
#         cursor = connection.cursor()

#         cursor.execute(f"SHOW DATABASES LIKE '{db_name}';")
#         result = cursor.fetchone()

#         if not result:
#             print(f"⚠️ Banco '{db_name}' não encontrado. Criando...")
#             cursor.execute(f"CREATE DATABASE {db_name};")
#             print("✅ Banco criado com sucesso.")
#         else:
#             print(f"✅ Banco '{db_name}' encontrado.")

#         connection.database = db_name

#         cursor.execute("SHOW TABLES LIKE 'users';")
#         table_exists = cursor.fetchone()

#         if not table_exists:
#             print("⚠️ Tabela 'users' não encontrada. Criando...")

#             engine = create_engine(f'mysql+mysqlconnector://root:root@localhost:3306/{db_name}')
#             from src.models.user_entity import User
#             Base.metadata.create_all(engine)

#             print("✅ Tabela 'users' criada com sucesso.")
#             restart_needed = True
#             cursor.close()
#             connection.close()
#             connection = get_mysql_connection()
#             cursor = connection.cursor()
#         else:
#             print("✅ Tabela 'users' encontrada.")
#             print("✅ Dados verificados e consistentes.")

#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("❌ Erro de autenticação: Verifique usuário/senha.")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("❌ Erro: Banco de dados não encontrado ou inválido.")
#         else:
#             print(f"❌ Erro desconhecido: {err}")
#         return None
#     finally:
#         cursor.close()
#         # connection.close()

#     # Se a tabela foi criada, reinicia o servidor
#     if restart_needed:
#         print("🔄 Criando dados necessários...")
#         time.sleep(1)  

#         print("✅ Criado com sucesso.")
#         print("🔄 Reiniciando servidor...")
#         time.sleep(2) 

#     else:
#         print("✅ Conectando ao MySQL...")
#         time.sleep(1)
#         print("✅ Servidor conectado.")

#     return connection

import time
import mysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.database.mysql.mysql import get_mysql_connection
from mysql.connector import errorcode

Base = declarative_base()

def setup_mysql_database():
    print("🔹 Inicializando conexão única com MySQL...")

    db_name = "user_db"

    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()

        cursor.execute(f"SHOW DATABASES LIKE '{db_name}';")
        result = cursor.fetchone()

        if not result:
            print(f"⚠️ Banco '{db_name}' não encontrado. Criando...")
            cursor.execute(f"CREATE DATABASE {db_name};")
            print("✅ Banco criado com sucesso.")
        
        connection.database = db_name

        cursor.execute("SHOW TABLES LIKE 'users';")
        if not cursor.fetchone():
            print("⚠️ Tabela 'users' não encontrada. Criando...")

            engine = create_engine(f'mysql+mysqlconnector://root:root@localhost:3306/{db_name}')
            from src.models.user_entity import User
            Base.metadata.create_all(engine)

            print("✅ Tabela 'users' criada com sucesso.")
        
        print("✅ Conexão MySQL pronta.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Erro de autenticação: Verifique usuário/senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("❌ Erro: Banco de dados inválido.")
        else:
            print(f"❌ Erro desconhecido: {err}")
        return None
