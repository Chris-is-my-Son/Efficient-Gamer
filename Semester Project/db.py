import sqlite3

def create_table():
    database = sqlite3.connect('application.db')
    cursor = database.cursor()
    table = '''CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT NOT NULL,
                isadmin BOOL DEFAULT False,
                createdat DEFAULT CURRENT_TIMESTAMP);'''
    cursor.execute(table)
    database.commit()

def insert_records(data):
    database = sqlite3.connect('application.db')
    cursor = database.cursor()
    insert = '''INSERT INTO users (id, username, email, password, isadmin)
                VALUES (?, ?, ?, ?, ?);'''
    cursor.executemany(insert, data)
    database.commit()

def update_admin(username, isadmin):
    database = sqlite3.connect('application.db')
    cursor = database.cursor()
    update = '''UPDATE users
                SET isadmin = ?
                WHERE
                username = ?;'''
    cursor.execute(update, (username, isadmin))
    database.commit()
    
def get_nonadmin_user():
    database = sqlite3.connect('application.db')
    cursor = database.cursor()
    select = '''SELECT username FROM users
                WHERE
                isadmin = 0;'''
    cursor.execute(select)
    nonadmin = cursor.fetchall()
    return nonadmin

def get_user(id):
    database = sqlite3.connect('application.db')
    cursor = database.cursor()
    select = '''SELECT * FROM users
                WHERE
                id = ? ;'''
    cursor.execute(select, (id,))
    user = cursor.fetchone()
    return user

def save_user(username,email,password, isadmin,id):
    success=True
    try:
        conn = sqlite3.connect('application.db')
        cur = conn.cursor()       
        cur.execute('''UPDATE users SET username =?, email=?, password=?, isadmin=? WHERE id=?''', (username,email,password,isadmin,id,))
        conn.commit()        
    except sqlite3.Error as err:
        print('save_user error', err)
        success=False
    finally:
        if conn != None:
            conn.close()
    return success

def delete_user_by_id(id):
    try:
        database = sqlite3.connect('application.db')
        cursor = database.cursor()
        delete = '''DELETE FROM users
                    WHERE
                    id = ?;'''
        cursor.execute(delete, (id,))
        database.commit()
        if database != None:
            database.close()
        return True
    except sqlite3.Error as err:
        print("Database Error", err)
        if database != None:
            database.close()
        return False

def check_user(username, password):
    user = None   
    database = sqlite3.connect('application.db')
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    
    return user
def get_all_users():
    users = None
    try:
        database = sqlite3.connect('application.db')
        cursor = database.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if database != None:
            database.close()
    return users

def add_user(user, email, password, isadmin):
    success=True
    try:
        database = sqlite3.connect('application.db')
        cursor = database.cursor()
        cursor.execute("INSERT INTO users (username, email, password,isadmin) VALUES (?,?,?,?)", (user,email,password,isadmin))
        database.commit()        
    except sqlite3.Error as err:
        print('Database Error', err)
        success=False
    finally:
        if database != None:
            database.close()
    return success

def register_user(user, email, password):
    success=True
    try:
        database = sqlite3.connect('application.db')
        cursor = database.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (user, email, password))
        database.commit()        
    except sqlite3.Error as err:
        print('Database Error', err)
        success=False
    finally:
        if database != None:
            database.close()
    return success