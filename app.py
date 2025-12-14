from flask import Flask, render_template, redirect, request, session, jsonify
import requests
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecret"
DISCORD_CLIENT_ID = "YOUR_CLIENT_ID"
DISCORD_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
DISCORD_REDIRECT_URI = "https://YOUR-RAILWAY-URL/auth/callback"

# ---- DATABASE ----
def db():
    return sqlite3.connect("database.db")

with db() as con:
    con.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT,
        premium INTEGER DEFAULT 0
    )""")

# ---- ROUTES ----
@app.route("/")
def home():
    if "user" not in session:
        return render_template("login.html")
    return redirect("/dashboard")

@app.route("/login")
def login():
    return redirect(
        f"https://discord.com/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code&scope=identify guilds"
    )

@app.route("/auth/callback")
def callback():
    code = request.args.get("code")

    token = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id": DISCORD_CLIENT_ID,
            "client_secret": DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": DISCORD_REDIRECT_URI
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()

    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    ).json()

    session["user"] = user

    with db() as con:
        con.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, 0)",
            (user["id"], user["username"])
        )

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html", user=session["user"])

@app.route("/api/premium")
def premium():
    user_id = session["user"]["id"]
    cur = db().cursor()
    cur.execute("SELECT premium FROM users WHERE id=?", (user_id,))
    return jsonify({"premium": cur.fetchone()[0] == 1})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/") 
