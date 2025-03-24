# import mysql.connector

# def get_mysql_connection():
#     return mysql.connector.connect(
#         user="root",
#         password="root",
#         host="localhost",
#         port=3306
#     )

import mysql.connector

mysql_connection = None  # Variável global para conexão

def get_mysql_connection():
    global mysql_connection
    if mysql_connection is None or not mysql_connection.is_connected():
        print("🔄 Criando nova conexão com MySQL...")
        mysql_connection = mysql.connector.connect(
            user="root",
            password="root",
            host="localhost",
            port=3306
        )

        # Agora garantimos que o banco de dados correto seja selecionado
        cursor = mysql_connection.cursor()
        cursor.execute("USE user_db;")
        cursor.close()

    return mysql_connection