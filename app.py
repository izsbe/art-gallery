import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, make_response
import config
#import db
import posts
import users
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_posts = posts.get_posts()
    return render_template("index.html", posts=all_posts)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    posts = users.get_posts(user_id)
    comments = users.count_comments(user_id)
    return render_template("show_user.html", user=user, posts=posts, comments=comments)

@app.route("/find_post")
def find_post():
    query_word = request.args.get("query_word", "")
    query_category = request.args.get("query_category", "")
    categories = posts.get_all_categories()

    if len(query_word) > 30:
            abort(403)

    if query_word or query_category:
        results = posts.find_posts(query_word, query_category)
    else:
        results = []

    return render_template("find_post.html",
                           query_word=query_word,
                           query_category=query_category,
                           categories=categories,
                           results=results)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    categories = posts.get_categories(post_id)
    comments = posts.get_comments(post_id)
    return render_template("show_post.html", post=post, categories=categories, comments=comments)

@app.route("/new_post")
def new_post():
    require_login()
    categories = posts.get_all_categories()
    return render_template("new_post.html", categories=categories)


@app.route("/create_post", methods=["POST"])
def create_post():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)

    file = request.files["image"]
    filename = file.filename.lower()
    if not (filename.endswith(".jpg") or filename.endswith(".jpeg")):
        return "ERROR: wrong file type"

    image = file.read()
    if len(image) > 100 * 1024:
        return "ERROR: image is too large"

    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)

    selected_categories = request.form.getlist("categories")
    if not selected_categories:
        abort(403)

    user_id = session["user_id"]

    posts.add_post(title, description, user_id, selected_categories, image)

    return redirect("/")

@app.route("/image/<int:post_id>")
def show_image(post_id):
    image = posts.get_image(post_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    comment = request.form["comment"]
    if not comment or len(comment) > 100:
        abort(403)
    post_id = request.form["post_id"]
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    user_id = session["user_id"]

    posts.add_comment(post_id, user_id, comment)

    return redirect("/post/" + str(post_id))

@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    require_login()

    comment = posts.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_comment.html", comment=comment)

    if request.method == "POST":
        check_csrf()

        content = request.form["content"]
        if not comment or len(comment) > 100:
            abort(403)

        posts.update_comment(comment["id"], content)
        return redirect("/post/" + str(comment["post_id"]))

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()

    comment = posts.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment)

    if request.method == "POST":
        check_csrf()

        if "continue" in request.form:
            posts.remove_comment(comment["id"])
        return redirect("/post/" + str(comment["post_id"]))

@app.route("/edit_post/<int:post_id>")
def edit_post(post_id):
    require_login()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)

    selected_categories = posts.get_categories(post_id)
    all_categories = posts.get_all_categories()

    return render_template(
        "edit_post.html",
        post=post,
        selected_categories=selected_categories,
        all_categories=all_categories
        )

@app.route("/update_post", methods=["POST"])
def update_post():
    require_login()
    check_csrf()

    post_id = request.form["post_id"]
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)

    selected_categories = request.form.getlist("categories")
    if not selected_categories:
        abort(403)

    posts.update_post(
        post_id,
        title,
        description,
        selected_categories
        )

    return redirect("/post/" + str(post_id))

@app.route("/remove_post/<int:post_id>", methods=["GET", "POST"])
def remove_post(post_id):
    require_login()

    post = posts.get_post(post_id)
    if not post:
        abort(404)

    if post["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_post.html", post=post)

    if request.method == "POST":
        check_csrf()

        if "remove" in request.form:
            posts.remove_post(post_id)
            return redirect("/")

        return redirect("/post/" + str(post_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "Passwords do not match"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "Username is already taken"

    return "Account created"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            session["username"] = username
            return redirect("/")
        else:
            return "Incorrect username or/and password"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")