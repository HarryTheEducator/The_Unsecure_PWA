import sqlite3 as sql
import time
import random
import bcrypt
from markupsafe import escape


def insertUser(username, password, DoB):
    # 1. Generate a salt (random data added to the password)
    salt = bcrypt.gensalt()
    # 2. Hash the password (one-way scramble)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    # 3. Insert the HASH instead of the raw password
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hashed_password.decode("utf-8"), DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    # Fetch ONLY the hashed password from the database for this user
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    con.close()
    if result:
        stored_hash = result[0].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return True
    return False


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{escape(row[1])}\n")  # Use escape() to neutralise scripts
        f.write("</p>\n")
    f.close()
