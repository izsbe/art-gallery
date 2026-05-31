import db

def add_item(title, description, user_id):
    sql = """INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)"""
    db.execute(sql, [title, description, user_id])