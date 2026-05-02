import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash

from database.db import create_user, get_db, get_user_by_email, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must be at least 8 characters.",
            )

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="An account with that email already exists.",
            )

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]
        user = get_user_by_email(email)
        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.")
        session["user_id"] = user["id"]
        return redirect(url_for("profile"))
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "January 2026",
    }

    stats = {
        "total_spent": "₹6,330",
        "transaction_count": 8,
        "top_category": "Shopping",
    }

    transactions = [
        {"date": "Apr 1, 2026",  "description": "Lunch at canteen",    "category": "Food",          "amount": "₹180"},
        {"date": "Apr 3, 2026",  "description": "Metro card recharge", "category": "Transport",     "amount": "₹500"},
        {"date": "Apr 5, 2026",  "description": "Electricity bill",    "category": "Bills",         "amount": "₹1,200"},
        {"date": "Apr 8, 2026",  "description": "Pharmacy",            "category": "Health",        "amount": "₹350"},
        {"date": "Apr 12, 2026", "description": "Movie tickets",       "category": "Entertainment", "amount": "₹600"},
        {"date": "Apr 15, 2026", "description": "New shoes",           "category": "Shopping",      "amount": "₹2,500"},
        {"date": "Apr 18, 2026", "description": "Miscellaneous",       "category": "Other",         "amount": "₹200"},
        {"date": "Apr 22, 2026", "description": "Dinner with friends", "category": "Food",          "amount": "₹800"},
    ]

    categories = [
        {"name": "Shopping",      "total": "₹2,500", "count": 1, "pct": 100},
        {"name": "Bills",         "total": "₹1,200", "count": 1, "pct": 48},
        {"name": "Food",          "total": "₹980",   "count": 2, "pct": 39},
        {"name": "Entertainment", "total": "₹600",   "count": 1, "pct": 24},
        {"name": "Transport",     "total": "₹500",   "count": 1, "pct": 20},
        {"name": "Health",        "total": "₹350",   "count": 1, "pct": 14},
        {"name": "Other",         "total": "₹200",   "count": 1, "pct": 8},
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
