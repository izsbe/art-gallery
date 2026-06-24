CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    created_at TEXT,
    image BLOB,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments(
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    content TEXT,
    created_at TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE post_categories (
    post_id INTEGER REFERENCES posts,
    category_id INTEGER REFERENCES categories,
    PRIMARY KEY (post_id, category_id)
);