import os
import requests
from flask import Blueprint, redirect, request, session, url_for

auth = Blueprint("auth", __name__)

DISCORD_API = "https://discord.com/api"

@auth.route("/login")
def login():
    params = {
        "client_id": os.getenv("DISCORD_CLIENT_ID"),
        "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
        "response_type": "code",
        "scope": "identify guilds"
    }
    url = f"{DISCORD_API}/oauth2/authorize"
    return redirect(f"{url}?"+ "&".join([f"{k}={v}" for k,v in params.items()]))

@auth.route("/login/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": os.getenv("DISCORD_CLIENT_ID"),
        "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(f"{DISCORD_API}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    token = r.json()["access_token"]

    user = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    session["user"] = user
    return redirect("/dashboard")
