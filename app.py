from flask import Flask
from flask import redirect, render_template, request, session
import config, db, forum, users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    threads = forum.get_threads()
    return render_template("index.html", threads=threads)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/thread/<int:id>")
def show_thread(id):
    thread = forum.get_thread(id)
    messages = forum.get_messages(id)
    return render_template("thread.html", thread=thread, messages=messages)

@app.route("/new_thread", methods=["POST"])
def new_thread():
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]

    thread_id = forum.add_thread(title, content, user_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/new_message", methods=["POST"])
def new_message():
    content = request.form["content"]
    user_id = session["user_id"]
    thread_id = request.form["thread_id"]

    forum.add_message(content, user_id, thread_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_message(id):
    message = forum.get_message(id)

    if request.method == "GET":
        return render_template("edit.html", message=message)

    if request.method == "POST":
        content = request.form["content"]
        forum.update_message(message["id"], content)
        return redirect("/thread/" + str(message["thread_id"]))

@app.route("/remove/<int:id>", methods=["GET", "POST"])
def remove_message(id):
    message = forum.get_message(id)

    if request.method == "GET":
        return render_template("remove.html", message=message)

    if request.method == "POST":
        if "continue" in request.form:
            forum.remove_message(message["id"])
        return redirect("/thread/" + str(message["thread_id"]))

@app.route("/new_user", methods=["POST"])
def new_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    if users.create_user(username, password1):
        return "Tunnus luotu"
    else:
        return "VIRHE: tunnus on jo varattu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    else:
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")