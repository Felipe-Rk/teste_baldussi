import mysql.connector

def get_mysql_connection():
    return mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",
        port=3306
    )
