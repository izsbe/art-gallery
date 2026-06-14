import db

def get_all_categories():
    sql = "SELECT title, value FROM categories ORDER BY id"
    result = db.query(sql)

    categories = {}
    for title, value in result:
        categories[title] = []
    for title, value in result:
        categories[title].append(value)

    return categories

def add_post(title, description, user_id, categories):
    sql = """INSERT INTO posts (title, description, user_id) VALUES (?, ?, ?)"""
    db.execute(sql, [title, description, user_id])

    post_id = db.last_insert_id()

    sql = "INSERT INTO post_categories (post_id, title, value) VALUES (?, ?, ?)"
    for title, value in categories:
        db.execute(sql, [post_id, title, value])

def get_categories(post_id):
    sql = "SELECT title, value FROM post_categories WHERE post_id = ?"
    return db.query(sql, [post_id])

def get_posts():
    sql = "SELECT id, title FROM posts ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT posts.id,
                    posts.title,
                    posts.description,
                    users.username,
                    users.id user_id
             FROM posts, users
             WHERE posts.user_id = users.id AND
                   posts.id = ?"""
    result = db.query(sql, [post_id])
    return result[0] if result else None

def update_post(post_id, title, description):
    sql = """UPDATE posts SET title = ?,
                              description = ?
                          WHERE id = ?"""
    db.execute(sql, [title, description, post_id])

def remove_post(post_id):
    sql = "DELETE FROM posts WHERE id = ?"
    db.execute(sql, [post_id])

def find_posts(query):
    sql = """SELECT id, title
             FROM posts
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])