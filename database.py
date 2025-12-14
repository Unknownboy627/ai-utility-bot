import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    premium INTEGER DEFAULT 0
)
""")

# Servers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS servers (
    guild_id TEXT PRIMARY KEY,
    premium INTEGER DEFAULT 0
)
""")

conn.commit()

def is_user_premium(user_id):
    cursor.execute("SELECT premium FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == 1

def set_user_premium(user_id, value: bool):
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, premium) VALUES (?, ?)",
        (user_id, int(value))
    )
    conn.commit()
