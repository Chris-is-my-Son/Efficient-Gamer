import sqlite3

def create_table():
    database = sqlite3.connect('reviews.db')
    cursor = database.cursor()
    table = '''CREATE TABLE "post" (
	            "id"	INTEGER,
                "username"	TEXT,
	            "title"	TEXT,
	            "review"	TEXT,
	            "createdat"	TEXT DEFAULT CURRENT_TIMESTAMP,
	            PRIMARY KEY("id"));'''
    cursor.execute(table)
    database.commit()

def get_all_reviews():
    reviews = None
    try:
        database = sqlite3.connect('reviews.db')
        cursor = database.cursor()
        cursor.execute("SELECT * FROM post")
        reviews = cursor.fetchall()
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if database != None:
            database.close()
    return reviews

def get_review(id):
    database = sqlite3.connect('reviews.db')
    cursor = database.cursor()
    select = '''SELECT * FROM post
                WHERE
                id = ? ;'''
    cursor.execute(select, (id,))
    review = cursor.fetchone()
    return review

def delete_review_by_id(id):
    try:
        database = sqlite3.connect('reviews.db')
        cursor = database.cursor()
        delete = '''DELETE FROM post
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

def make_review(username, title, review):
    success=True
    try:
        database = sqlite3.connect('reviews.db')
        cursor = database.cursor()
        insert = '''INSERT INTO post (username, title, review)
                    VALUES (?,?,?)'''
        cursor.execute(insert, (username, title, review))
        database.commit()        
    except sqlite3.Error as err:
        print('Database Error', err)
        success=False
    finally:
        if database != None:
            database.close()
    return success

def update_review(title, review, id):
    success=True
    try:
        database = sqlite3.connect('reviews.db')
        cursor = database.cursor()
        update = '''UPDATE post
                    SET title = ?, review = ?
                    WHERE id=?'''
        cursor.execute(update, (title, review, id,))
        database.commit()        
    except sqlite3.Error as err:
        print('save_user error', err)
        success=False
    finally:
        if database != None:
            database.close()
    return success
   
def check_user(username, password):
    user = None
    database = sqlite3.connect('reviews.db')
    cursor = database.cursor()
    cursor.execute("SELECT * FROM post WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    return user