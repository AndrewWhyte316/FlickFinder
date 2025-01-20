from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import bcrypt

app=Flask(__name__)
DATABASE = 'FlickFinder.db'

# Database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Access rows as dictionaries
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Routes
@app.route("/")
def Home_Page():
    return render_template("home.html")

@app.route("/Index")
@app.route("/index.html")
def Index():
    return render_template("index.html")

@app.route("/Signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']
        db = get_db()
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db.execute("""
                INSERT INTO users (name, email, login, password)
                VALUES (?, ?, ?, ?)
            """, (name, email, login, hashed_password))
            db.commit()
            return redirect(url_for('Home_Page'))
        except sqlite3.IntegrityError:
            return "Login or email already exists!", 400
    return render_template("signup.html")

@app.route("/Login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        db = get_db()

        # Checks the database
        user = db.execute("""
            SELECT * FROM users WHERE login = ? AND password = ?
        """, (login, password)).fetchone()

        # Checks if the user exists and the password is correct
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Successful login
            return redirect(url_for('Home_Page'))
        return "Invalid login or password!", 401
    return render_template("login.html")

@app.route("/Recommendations")
def recommendations():
    db = get_db()
    genres = db.execute("SELECT * FROM genres").fetchall()
    return render_template("recommendations.html", genres=genres)

@app.route("/Recommendations/<genre>")
def randomgenre(genre):
    db = get_db()
    movie = db.execute("""
        SELECT title FROM movies
        JOIN genres ON movies.genre_id = genres.id
        WHERE genres.name = ?
        ORDER BY RANDOM() LIMIT 1
    """, (genre,)).fetchone()
    if movie:
        return render_template("genre.html", movie=movie['title'], genre=genre)
    return f"No movies found for genre: {genre}", 404

if __name__ == "__main__":
    app.run(debug=True)