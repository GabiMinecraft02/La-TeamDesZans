from flask import Flask, render_template, redirect, request, session
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# mots de passe (exemple simple)
MEMBER_PASSWORD = os.getenv("PASSWORD", "member123")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


# ---------- PAGES PUBLIQUES ----------

@app.route("/")
def home():
    return render_template("index.html")


# ---------- MEMBRES ----------

@app.route("/memberslogin", methods=["GET", "POST"])
def members_login():
    if request.method == "POST":
        if request.form["password"] == MEMBER_PASSWORD:
            session["member"] = True
            return redirect("/members")
        else:
            return render_template("MLogin.html", error="Mot de passe incorrect")

    return render_template("MLogin.html")


@app.route("/members")
def members():
    if not session.get("member"):
        return redirect("/memberslogin")
    return render_template("members.html")


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
    app.run(debug=True)
