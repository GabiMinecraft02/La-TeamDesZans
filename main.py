from flask import Flask, render_template, redirect, request, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# mots de passe (exemple simple)
MEMBER_PASSWORD = os.getenv("PASSWORD", "member123")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

EVENTS = [
    {
        "title": "Admin Abuse",
        "days": [1],
        "start": "23:00",
        "end": "23:30",
        "description": "Admin abuse"
    },
    {
        "title": "Admin Abuse",
        "days": [5],
        "start": "21:00",
        "end": "21:30",
        "description": "Admin abuse"
    }
]

# ---------- MEMBRES ----------

@app.route("/", methods=["GET", "POST"])
def members_login():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]

        if password == MEMBER_PASSWORD:
            session["member"] = True
            session["pseudo"] = pseudo  # <- on stocke le pseudo
            return redirect("/members")
        else:
            return render_template("MLogin.html", error="Mot de passe incorrect")

    return render_template("MLogin.html")


@app.route("/members")
def members():
    if not session.get("member"):
        return redirect("/")

    now = datetime.now()
    current_day = now.weekday()      # 0-6
    current_time = now.strftime("%H:%M")

    current_event = None

    for event in EVENTS:
        if current_day in event["days"]:
            if event["start"] <= current_time <= event["end"]:
                current_event = event
                break

    day_names = [
        "lundi", "mardi", "mercredi",
        "jeudi", "vendredi", "samedi", "dimanche"
    ]

    pseudo = session.get("pseudo", "Utilisateur")

    return render_template(
        "members.html",
        event=current_event,
        now=now.strftime("%H:%M"),
        today=day_names[current_day],
        pseudo=pseudo  # <- on envoie le pseudo au template
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------- ADMIN ----------

@app.route("/adminlogin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        else:
            return render_template("adminlogin.html", error="Mot de passe incorrect")

    return render_template("adminlogin.html")


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/adminlogin")
    return render_template("admin.html")


# ---------- RUN ----------

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
