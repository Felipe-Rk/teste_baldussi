from src.database.mysql.mysql_config import setup_mysql_database

def get_users(page=1, per_page=10):
    conect = setup_mysql_database()
    cursor = conect.cursor(dictionary=True)
    
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM users LIMIT %s OFFSET %s", (per_page, offset))
    users = cursor.fetchall()
    
    cursor.close()
    conect.close()
    return users

def get_user_id(user_id):
    conect = setup_mysql_database()
    cursor = conect.cursor(dictionary = True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conect.close()
    return user

def update_user_service(user_id, updates):
    conect = setup_mysql_database()
    cursor = conect.cursor()
    set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
    query = f"UPDATE users SET {set_clause} WHERE id = %s"
    values = list(updates.values()) + [user_id]
    cursor.execute(query, values)
    conect.commit()
    cursor.close()
    conect.close()
    return True

def delete_user_service(user_id):
    conect = setup_mysql_database()
    cursor = conect.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id, ))
    conect.commit()
    cursor.close()
    conect.close()
    return True