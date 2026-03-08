from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "hostel_secret"


# DATABASE CREATE
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    room_type TEXT,
    stay_type TEXT,
    hours INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("SELECT * FROM users WHERE username='admin'")
admin = cursor.fetchone()

if not admin:
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "1234")
    )

conn.commit()
conn.close()


# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ADMIN LOGIN
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":

            session["admin"] = True
            return redirect("/dashboard")

        else:
            return "Invalid Login"

    return render_template("admin_login.html")


# ADD BOOKING
@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form["name"]
        room_type = request.form["room_type"]
        stay_type = request.form["stay_type"]
        hours = request.form["hours"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO bookings (name, room_type, stay_type, hours) VALUES (?,?,?,?)",
            (name, room_type, stay_type, hours)
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_booking.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total = cursor.fetchone()[0]

    total_rooms = 20
    available = total_rooms - total

    conn.close()

    return render_template(
        "dashboard.html",
        rows=rows,
        total=total,
        booked=total,
        available=available
    )


# DELETE BOOKING
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# EDIT BOOKING
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        room_type = request.form["room_type"]

        cur.execute(
            "UPDATE bookings SET name=?, room_type=? WHERE id=?",
            (name, room_type, id)
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    cur.execute("SELECT * FROM bookings WHERE id=?", (id,))
    booking = cur.fetchone()

    conn.close()

    return render_template("edit.html", booking=booking)


# PAYMENT PAGE
@app.route("/payment/<int:id>")
def payment(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings WHERE id=?", (id,))
    booking = cursor.fetchone()

    conn.close()

    return render_template("payment.html", booking=booking)


# SUCCESS PAGE
@app.route("/success")
def success():
    return render_template("success.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)