from werkzeug.security import generate_password_hash, check_password_hash
import db

def create_user(username, password1):
    password_hash = generate_password_hash(password1)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_posts(user_id):
    sql = "SELECT id, title FROM posts WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def count_comments(user_id):
    sql = "SELECT COUNT(id) AS comment_count FROM comments WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0]["comment_count"] if result else 0

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return None