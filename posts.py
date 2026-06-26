import db
from datetime import datetime

def get_all_categories():
    sql = "SELECT id, name FROM categories ORDER BY name"
    return db.query(sql)

def add_post(title, description, user_id, categories, image):
    created_at = datetime.now().strftime("%d/%m/%Y, %H:%M")
    sql = "INSERT INTO posts (title, description, created_at, image, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, description, created_at, image,  user_id])

    post_id = db.last_insert_id()

    sql = "INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)"

    for category_id in categories:
        db.execute(sql, [post_id, category_id])

def get_image(post_id):
    sql = "SELECT image FROM posts WHERE id = ?"
    result = db.query(sql, [post_id])

    if not result:
        return None

    return result[0]["image"]

def add_comment(post_id, user_id, comment):
    created_at = datetime.now().strftime("%d/%m/%Y, %H:%M")
    sql = "INSERT INTO comments (post_id, user_id, content, created_at) VALUES (?, ?, ?, ?)"
    db.execute(sql, [post_id, user_id, comment, created_at])

def get_comments(post_id):
    sql = """SELECT comments.id,
                    comments.content,
                    comments.created_at,
                    users.id user_id,
                    users.username
             FROM comments, users
             WHERE comments.post_id = ? AND comments.user_id = users.id
             ORDER BY comments.id DESC"""
    return db.query(sql, [post_id])

def get_comment(comment_id):
    sql = """SELECT id,
                    content,
                    post_id,
                    user_id
             FROM comments
             WHERE id = ?"""

    result = db.query(sql, [comment_id])
    return result[0] if result else None

def update_comment(comment_id, content):
    sql = "UPDATE comments SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def get_categories(post_id):
    sql = """SELECT categories.id,
                    categories.name
             FROM categories, post_categories
             WHERE categories.id = post_categories.category_id
                AND post_categories.post_id = ?
             ORDER BY categories.name"""

    return db.query(sql, [post_id])

def get_posts():
    sql = "SELECT id, title FROM posts ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT posts.id,
                    posts.title,
                    posts.description,
                    posts.created_at,
                    users.username,
                    users.id user_id
             FROM posts, users
             WHERE posts.user_id = users.id AND
                   posts.id = ?"""
    result = db.query(sql, [post_id])
    return result[0] if result else None

def update_post(post_id, title, description, categories):
    sql = """UPDATE posts
             SET title = ?,
                 description = ?
             WHERE id = ?"""

    db.execute(sql, [title, description, post_id])

    sql = "DELETE FROM post_categories WHERE post_id = ?"
    db.execute(sql, [post_id])

    sql = "INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)"
    for category_id in categories:
        db.execute(sql, [post_id, category_id])

def remove_post(post_id):
    sql = "DELETE FROM post_categories WHERE post_id = ?"
    db.execute(sql, [post_id])
    sql = "DELETE FROM posts WHERE id = ?"
    db.execute(sql, [post_id])

def find_posts(query_word, query_category):
    sql = """SELECT DISTINCT posts.id, posts.title
             FROM posts
             LEFT JOIN post_categories ON posts.id = post_categories.post_id
             WHERE 1=1"""

    params = []

    if query_word:
        sql += " AND (posts.title LIKE ? OR posts.description LIKE ?)"
        like = "%" + query_word + "%"
        params.extend([like, like])

    if query_category:
        sql += " AND post_categories.category_id = ?"
        params.append(query_category)

    sql += " ORDER BY posts.id DESC"

    return db.query(sql, params)