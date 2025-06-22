from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime
import random  # <-- if not already there
import pytz


LOVE_QUOTES = [
    "Every moment with you is a dream come true.",
    "You are my today and all of my tomorrows.",
    "I fall in love with you more every day.",
    "You're the best part of my world.",
    "You're the reason I believe in love again.",
]

app = Flask(__name__)
JOURNAL_FILE = "journal.json"

def is_birthday():
    today = datetime.now().strftime('%m-%d')
    return today == '08-30'

def load_entries():
    if not os.path.exists(JOURNAL_FILE):
        return []
    with open(JOURNAL_FILE, "r") as f:
        return json.load(f)

def save_entries(entries):
    with open(JOURNAL_FILE, "w") as f:
        json.dump(entries, f, indent=4)

from datetime import datetime

@app.route("/")
def home():
    quote = random.choice(LOVE_QUOTES)

    # Calculate countdown to August 30th, this year or next year if passed
    now = datetime.now()
    current_year = now.year
    birthday = datetime(current_year, 8, 30)

    # If birthday already passed this year, use next year
    if now > birthday:
        birthday = datetime(current_year + 1, 8, 30)

    diff = birthday - now

    days = diff.days
    seconds_left = diff.seconds
    hours = seconds_left // 3600
    minutes = (seconds_left % 3600) // 60
    seconds = seconds_left % 60

    return render_template(
        "index.html",
        quote=quote,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )


@app.route("/journal")
def journal():
    print("📝 /journal route loaded")
    entries = load_entries()
    print("Entries:", entries)

    # Check if today is August 30
    today = datetime.now()
    is_birthday = (today.month == 8 and today.day == 30)

    return render_template("journal.html", entries=entries, is_birthday=is_birthday)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    message = request.form["message"]
    mood = request.form.get("mood", "")
    private_note = request.form.get("private_note", "")

    import pytz
    mytz = pytz.timezone('Asia/Kuala_Lumpur')
    date = datetime.now(mytz).strftime("%Y-%m-%d %H:%M")

    entries = load_entries()
    entries.insert(0, {
        "id": datetime.now().timestamp(),
        "title": title,
        "message": message,
        "mood": mood,
        "private_note": private_note,
        "date": date
    })
    save_entries(entries)
    return redirect(url_for("journal"))

@app.route("/delete/<float:entry_id>")
def delete(entry_id):
    entries = load_entries()
    entries = [e for e in entries if e["id"] != entry_id]
    save_entries(entries)
    return redirect(url_for("journal"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)      
