from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/")
def home():
    return "SQL Security Project is running!"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        conn.commit()
        conn.close()
        return "Регистрацията е успешна!"
    
    return render_template_string("""
    <h2>Регистрация</h2>
    <form method="POST">
      Потребител: <input name="username"><br>
      Парола: <input name="password" type="password"><br>
      <input type="submit" value="Регистрирай се">
    </form>
    """)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        user = c.fetchone()
        conn.close()

        if user:
            return f"Успешен login! Добре дошла, {username}"
        else:
            return "Грешно потребителско име или парола!"
    
    return render_template_string("""
    <h2>Login</h2>
    <form method="POST">
      Потребител: <input name="username"><br>
      Парола: <input name="password" type="password"><br>
      <input type="submit" value="Вход">
    </form>
    """)

comments = []

@app.route("/comment", methods=["GET", "POST"])
def comment():
    global comments

    if request.method == "POST":
        text = request.form["text"]
        comments.append(text)

    page = "<h2>Comments</h2>"

    page += """
    <form method="POST">
    Напиши коментар: <input name="text">
    <input type="submit" value="Post">
    </form>
    <br><br>
    """

    for c in comments:
        page += f"<p>{c}</p>"

    return page

if __name__ == "__main__":
    app.run(debug=True)