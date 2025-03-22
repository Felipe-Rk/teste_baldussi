from src.database.mysql.mysql_config import setup_mysql_database

def get_users():
    conect = setup_mysql_database()
    cursor = conect.cursor(dictionary = True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conect.close()
    return users

def get_user_id(user_id):
    conect = setup_mysql_database()
    cursor = conect.cursor(dictionary = True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id))
    user = cursor.fetchone()
    cursor.close()
    conect.close()
    return user

def update_user(user_id, updates):
    conect = setup_mysql_database()
    cursor = conect.cursor()
    query = "UPDATE users SET"
    query += ", ".join([f"{key} = %s" for key in updates.keys()])
    values = list(updates.value()) + [user_id]
    cursor.execute(query, values)
    conect.commit()
    cursor.close()
    conect.close()
    return True

def delete_user(user_id):
    conect = setup_mysql_database()
    cursor = conect.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id, ))
    conect.commit()
    cursor.close()
    conect.close()
    return True