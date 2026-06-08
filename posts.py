import db

def add_post(title, description, user_id):
    sql = """INSERT INTO posts (title, description, user_id) VALUES (?, ?, ?)"""
    db.execute(sql, [title, description, user_id])