from flask import Flask, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "rates.db"

ADMIN_PASSWORD = "LJ@2026"   # 🔐 change this later

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS rates(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gold22 REAL,
            gold24 REAL,
            silver REAL,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT gold22,gold24,silver,updated_at FROM rates ORDER BY id DESC LIMIT 1")
    rate = c.fetchone()
    conn.close()

    if not rate:
        return "<h2 style='text-align:center;margin-top:50px;'>Rates Not Updated Yet</h2>"

    return f"""
    <html>
    <head>
    <title>Londhe Jewelers - Gold Rate</title>
    <style>
        body {{
            font-family: Arial;
            background: linear-gradient(to bottom, #000000, #1a1a1a);
            color: white;
            text-align: center;
        }}
        .card {{
            background: #111;
            margin: 100px auto;
            padding: 40px;
            width: 400px;
            border-radius: 15px;
            box-shadow: 0 0 20px gold;
        }}
        h1 {{
            color: gold;
        }}
        .rate {{
            font-size: 22px;
            margin: 15px 0;
        }}
        .update {{
            font-size: 12px;
            color: #aaa;
            margin-top: 20px;
        }}
    </style>
    </head>
    <body>
        <div class="card">
            <h1>Londhe Jewelers</h1>
            <div class="rate">22K Gold: ₹ {rate[0]}</div>
            <div class="rate">24K Gold: ₹ {rate[1]}</div>
            <div class="rate">Silver: ₹ {rate[2]}</div>
            <div class="update">Last Updated: {rate[3]}</div>
            <br>
            <div>📍 Khamla Road, Nagpur</div>
            <div>📞 9373116054</div>
        </div>
    </body>
    </html>
    """

@app.route("/update", methods=["GET","POST"])
def update():
    if request.method == "POST":
        password = request.form["password"]
        if password != ADMIN_PASSWORD:
            return "❌ Wrong Password"

        gold22 = request.form["gold22"]
        gold24 = request.form["gold24"]
        silver = request.form["silver"]

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO rates(gold22,gold24,silver,updated_at) VALUES(?,?,?,?)",
                  (gold22, gold24, silver,
                   datetime.now().strftime("%d-%m-%Y %I:%M %p")))
        conn.commit()
        conn.close()

        return redirect("/")

    return """
    <h2>Admin Login - Update Rate</h2>
    <form method="post">
        Password: <input type="password" name="password"><br><br>
        22K Gold: <input name="gold22"><br><br>
        24K Gold: <input name="gold24"><br><br>
        Silver: <input name="silver"><br><br>
        <button type="submit">Update</button>
    </form>
    """

if __name__ == "__main__":
    init_db()
    app.run(debug=True)