from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management
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

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.execute("""
                INSERT INTO users (name, email, username, password)
                VALUES (?, ?, ?, ?)
            """, (name, email, username, hashed_password))
            db.commit()
            return redirect(url_for('Home_Page'))
        except sqlite3.IntegrityError:
            return "Username or email already exists!", 400
    return render_template("signup.html")

@app.route("/Login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()  # Forget any user_id

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password were submitted
        if not username:
            return "Must provide username!", 403
        if not password:
            return "Must provide password!", 403

        db = get_db()
        user = db.execute("""
            SELECT * FROM users WHERE username = ?
        """, (username,)).fetchone()

        if user:
            stored_password = user['password']  # Retrieved as a string from the database

            # Ensure the stored password is encoded to bytes
            if isinstance(stored_password, str):
                stored_password = stored_password.encode('utf-8')

            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                session["user_id"] = user["id"]  # Remember the logged-in user
                return redirect("/")
            else:
                print("DEBUG: Password does not match!")
        else:
            print("DEBUG: Username not found!")

        return "Invalid username or password!", 403

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")

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

@app.route("/Aboutus")
def about_us():
    """About Us page"""
    return render_template("info.html")

@app.route("/Filmshowings/")
def film_showings():
    """Film Times page"""
    # Example data (replace with your actual database query results)
    headings = ["Film", "Time", "Location"]
    show = [("film1", "Inception", "7:00 PM"), ("film2", "Avatar", "9:00 PM")]
    time = [("t1", "10:00 AM", "Morning"), ("t2", "8:00 PM", "Evening")]
    location = [("loc1", "Cinema 1", "Cambridge", "123 Main St"),
                ("loc2", "Cinema 2", "Boston", "456 Elm St")]

    # Render the template with data
    return render_template("showtimes.html", headings=headings, show=show, time=time, location=location)

@app.route("/Profile", methods=["GET", "POST"])
def profile():
    """User profile page for updating information"""
    if "user_id" not in session:
        return redirect(url_for("login"))  # Redirect to login if not logged in

    db = get_db()

    if request.method == "POST":
        # Handle profile updates
        location = request.form.get("location")
        password = request.form.get("password")

        # Update location if provided
        if location:
            db.execute("""
                UPDATE users SET location = ? WHERE id = ?
            """, (location, session["user_id"]))

        # Update password if provided
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.execute("""
                UPDATE users SET password = ? WHERE id = ?
            """, (hashed_password, session["user_id"]))

        db.commit()
        return redirect(url_for("profile"))  # Reload the profile page with updated info

    # Render profile page with existing data
    user = db.execute("""
        SELECT * FROM users WHERE id = ?
    """, (session["user_id"],)).fetchone()

    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)