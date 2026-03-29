import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "blooddonor2024")


# ──────────────────────────────────────────────
# Database connection
# ──────────────────────────────────────────────
def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "blooddonor"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "59F21a0463@123AP40BX3122"),
        port=os.environ.get("DB_PORT", "5432"),
    )


def init_db():
    """Create tables if they don't exist yet."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id          SERIAL PRIMARY KEY,
            name        VARCHAR(100) NOT NULL,
            phone       VARCHAR(20),
            blood_group VARCHAR(5)  NOT NULL,
            city        VARCHAR(100),
            created_at  TIMESTAMP   DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS blood_requests (
            id           SERIAL PRIMARY KEY,
            patient_name VARCHAR(100) NOT NULL,
            hospital     VARCHAR(200),
            blood_group  VARCHAR(5)  NOT NULL,
            urgency      VARCHAR(20),
            city         VARCHAR(100),
            created_at   TIMESTAMP   DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


# Auto-create tables on startup
with app.app_context():
    try:
        init_db()
    except Exception as e:
        print(f"DB init warning: {e}")


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.route("/")
def home():
    print("its Fayaz app") 
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM donors")
    total_donors = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM blood_requests")
    total_requests = cur.fetchone()[0]
    cur.close()
    conn.close()
    return render_template("index.html",
                           total_donors=total_donors,
                           total_requests=total_requests)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO donors (name, phone, blood_group, city)
               VALUES (%s, %s, %s, %s)""",
            (
                request.form["name"],
                request.form["phone"],
                request.form["blood_group"],
                request.form["city"],
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Thank you! You are registered as a donor.", "success")
        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/request-blood", methods=["GET", "POST"])
def request_blood():
    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO blood_requests
               (patient_name, hospital, blood_group, urgency, city)
               VALUES (%s, %s, %s, %s, %s)""",
            (
                request.form["patient_name"],
                request.form["hospital"],
                request.form["blood_group"],
                request.form["urgency"],
                request.form["city"],
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Blood request submitted successfully!", "success")
        return redirect(url_for("nearby_donors"))
    return render_template("request.html")


@app.route("/donors")
def nearby_donors():
    blood_filter = request.args.get("blood_group", "")
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if blood_filter:
        cur.execute(
            "SELECT * FROM donors WHERE blood_group = %s ORDER BY created_at DESC",
            (blood_filter,),
        )
    else:
        cur.execute("SELECT * FROM donors ORDER BY created_at DESC")
    donors = cur.fetchall()

    cur.execute("SELECT * FROM blood_requests ORDER BY created_at DESC")
    blood_requests = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("donors.html",
                           donors=donors,
                           requests=blood_requests,
                           blood_filter=blood_filter)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)