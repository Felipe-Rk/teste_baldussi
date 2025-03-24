from src.database.mysql.mysql import get_mysql_connection

def get_users(page=1, per_page=10, admin=False):
    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)

    offset = (page - 1) * per_page

    if admin:
        cursor.execute("SELECT id, cpf, nome, email, role FROM users LIMIT %s OFFSET %s", (per_page, offset))
    else:
        cursor.execute("SELECT id, cpf, nome, email FROM users WHERE role = 'user' LIMIT %s OFFSET %s", (per_page, offset))

    users = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) as total FROM users")
    total = cursor.fetchone()["total"]

    cursor.close()
    connection.close()

    return users, total

def get_user_id(user_id):
    conect = get_mysql_connection()
    cursor = conect.cursor(dictionary = True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conect.close()
    return user

def update_user_service(user_id, updates):
    conect = get_mysql_connection()
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
    conect = get_mysql_connection()
    cursor = conect.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id, ))
    conect.commit()
    cursor.close()
    conect.close()
    return True