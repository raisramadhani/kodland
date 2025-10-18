from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
import sqlite3
import hashlib
import random
import requests
from datetime import datetime, timedelta
import os
from config import Config

app = Flask(__name__)

config = Config()
app.config.from_object(config)
app.secret_key = config.SECRET_KEY


def init_db():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            total_score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        )
    """
    )

    sample_questions = [
        (
            "Apa itu Machine Learning dalam konteks aplikasi Python?",
            "Bahasa pemrograman baru",
            "Subset dari AI yang memungkinkan komputer belajar dari data",
            "Framework web Python",
            "Database management system",
            "B",
        ),
        (
            "Library Python mana yang paling populer untuk machine learning?",
            "Django",
            "Flask",
            "Scikit-learn",
            "Requests",
            "C",
        ),
        (
            "Apa fungsi utama dari TensorFlow dalam aplikasi AI Python?",
            "Web development",
            "Deep learning dan neural networks",
            "Database management",
            "API testing",
            "B",
        ),
        (
            "Apa itu supervised learning?",
            "Pembelajaran tanpa data",
            "Pembelajaran dengan data berlabel",
            "Pembelajaran mandiri",
            "Pembelajaran online",
            "B",
        ),
        (
            "Library Python mana yang digunakan untuk natural language processing?",
            "NumPy",
            "Pandas",
            "NLTK",
            "Matplotlib",
            "C",
        ),
        (
            "Apa itu neural network?",
            "Jaringan komputer",
            "Model komputasi yang terinspirasi dari otak manusia",
            "Database relational",
            "Web framework",
            "B",
        ),
        (
            "Fungsi utama dari library Pandas dalam AI adalah?",
            "Visualisasi data",
            "Manipulasi dan analisis data",
            "Web scraping",
            "Game development",
            "B",
        ),
        (
            "Apa itu deep learning?",
            "Pembelajaran mendalam tentang Python",
            "Subset ML yang menggunakan neural network berlapis",
            "Metode debugging",
            "Framework web",
            "B",
        ),
        (
            "Library mana yang digunakan untuk computer vision di Python?",
            "OpenCV",
            "Flask",
            "Django",
            "SQLite",
            "A",
        ),
        (
            "Apa itu API dalam konteks aplikasi AI?",
            "Artificial Programming Interface",
            "Application Programming Interface",
            "Automated Python Integration",
            "Advanced Programming Instructions",
            "B",
        ),
    ]

    cursor.execute("SELECT COUNT(*) FROM quiz_questions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """
            INSERT INTO quiz_questions (question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            sample_questions,
        )

    conn.commit()
    conn.close()


def get_weather_forecast(city):
    api_key = app.config.get("WEATHER_API_KEY")
    base_url = app.config.get("WEATHER_API_URL")

    if not api_key or api_key == "YOUR_API_KEY":
        print("Warning: Weather API key not properly configured")
        return get_fallback_weather(city)

    try:
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "cnt": 24,
        }

        response = requests.get(base_url, params=params)

        print(f"Weather API Request: {response.url}")
        print(f"Weather API Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            forecast = []
            today = datetime.now()

            for i in range(3):
                date = today + timedelta(days=i)
                day_name = date.strftime("%A")
                date_str = date.strftime("%Y-%m-%d")

                day_temp = (
                    data["list"][i * 8]["main"]["temp"]
                    if i * 8 < len(data["list"])
                    else 25
                )
                night_temp = (
                    data["list"][i * 8 + 4]["main"]["temp"]
                    if i * 8 + 4 < len(data["list"])
                    else 20
                )
                description = (
                    data["list"][i * 8]["weather"][0]["description"]
                    if i * 8 < len(data["list"])
                    else "Clear"
                )

                forecast.append(
                    {
                        "day": day_name,
                        "date": date_str,
                        "day_temp": round(day_temp),
                        "night_temp": round(night_temp),
                        "description": description.title(),
                    }
                )

            return forecast
        else:
            print(f"Weather API Error: {response.status_code} - {response.text}")
            return get_fallback_weather(city)
    except Exception as e:
        print(f"Weather API Exception: {str(e)}")
        return get_fallback_weather(city)


def get_fallback_weather(city):
    today = datetime.now()
    forecast = []
    for i in range(3):
        date = today + timedelta(days=i)
        day_name = date.strftime("%A")
        date_str = date.strftime("%Y-%m-%d")

        forecast.append(
            {
                "day": day_name,
                "date": date_str,
                "day_temp": 28 + i,
                "night_temp": 22 + i,
                "description": "Partly Cloudy",
            }
        )
    return forecast


@app.route("/")
def home():
    city = request.args.get("city", app.config.get("DEFAULT_CITY", "Jakarta"))
    weather_data = get_weather_forecast(city)
    current_date = datetime.now().strftime("%A, %d %B %Y")

    return render_template(
        "home.html", weather_data=weather_data, city=city, current_date=current_date
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Password tidak cocok!", "error")
            return render_template("register.html")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = sqlite3.connect("quiz_app.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            conn.commit()
            conn.close()

            flash("Pendaftaran berhasil! Silakan login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username sudah digunakan!", "error")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("quiz_app.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, total_score FROM users WHERE username = ? AND password = ?",
            (username, hashed_password),
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["total_score"] = user[2]
            flash("Login berhasil!", "success")
            return redirect(url_for("quiz"))
        else:
            flash("Username atau password salah!", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout berhasil!", "success")
    return redirect(url_for("home"))


@app.route("/quiz")
def quiz():
    if "user_id" not in session:
        flash("Silakan login terlebih dahulu!", "error")
        return redirect(url_for("login"))

    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_questions ORDER BY RANDOM() LIMIT 1")
    question = cursor.fetchone()
    conn.close()

    if question:
        question_data = {
            "id": question[0],
            "question": question[1],
            "options": [question[2], question[3], question[4], question[5]],
            "correct_answer": question[6],
        }
        return render_template("quiz.html", question=question_data)
    else:
        flash("Tidak ada pertanyaan tersedia!", "error")
        return redirect(url_for("home"))


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Not logged in"})

    answer = request.form["answer"]
    question_id = request.form["question_id"]

    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT correct_answer FROM quiz_questions WHERE id = ?", (question_id,)
    )
    correct_answer = cursor.fetchone()[0]

    is_correct = answer == correct_answer

    if is_correct:
        cursor.execute(
            "UPDATE users SET total_score = total_score + 10 WHERE id = ?",
            (session["user_id"],),
        )
        session["total_score"] += 10
        conn.commit()

    conn.close()

    return jsonify(
        {
            "success": True,
            "correct": is_correct,
            "correct_answer": correct_answer,
            "new_score": session["total_score"],
        }
    )


@app.route("/leaderboard")
def leaderboard():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, total_score FROM users ORDER BY total_score DESC LIMIT 10"
    )
    users = cursor.fetchall()
    conn.close()

    return render_template("leaderboard.html", users=users)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
