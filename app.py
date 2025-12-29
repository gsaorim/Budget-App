from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, usd


# Configure application
app = Flask(__name__)


# Custom filter
app.jinja_env.filters["usd"] = usd


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """ Manage the spendings """

    user_id = session["user_id"]

    if request.method == "POST":

        category = request.form.get("category")
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")

        # If they are null
        if not category:
            return apology("must provide category", 400)

        if not year:
            return apology("must provide year", 400)

        # Convert the strings to integers
        year = int(year)

        # Identify errors
        if year < 0:
            return apology("year must be positive", 400)

        # Convert back to string for the db params
        year = str(year)

    else:
        from datetime import datetime
        today = datetime.today()
        year = str(today.year)
        month = "all"
        day = "all"
        category = "all"


    # First start with query that always filter
    filters = "WHERE user_id = ? AND year = ? "
    params = [user_id, year]

    # Then after add the optional filters
    # Optional: add month filter
    if month != "all":
        filters += "AND month = ? "
        params.append(month)

    # Optional: add day filter
    if day != "all":
        filters += " AND day = ?"
        params.append(day)

    # Optional: add category filter
    if category != "all":
        filters += " AND category = ?"
        params.append(category)

    # Get all the transactions (reusing the filters)
    query = ("SELECT year, month, day, category, amount, note FROM transactions " \
            + filters + " ORDER BY year DESC, month DESC, day DESC")

    dashboards = db.execute(query, *params)

    # Get the totals
    sum_query = ("SELECT SUM(amount) AS total_expenses FROM transactions " + filters)

    row = db.execute(sum_query, *params)
    total_expenses = row[0]["total_expenses"] or 0

    # Get salary
    salary_row = db.execute("SELECT salary FROM users WHERE id = ?", user_id)
    salary = salary_row[0]["salary"] or 0

    # Get savings
    savings = salary - total_expenses

    # Return Template
    return render_template(
        "dashboard.html",
        dashboards=dashboards,
        salary=salary,
        total_expenses=total_expenses,
        savings=savings,
        year=year,
        month=month,
        day=day,
        category=category
    )



@app.route("/transaction", methods=["GET", "POST"])
@login_required
def transaction():
    """ Register the transactions """

    user_id = session["user_id"]

    if request.method == "POST":
        form_type = request.form.get("form_type")

        # Hadle salary
        if form_type == "salary":

            salary = request.form.get("salary")

            if not salary:
                return apology("must provide a salary", 400)

            db.execute("UPDATE users SET salary = ? WHERE id = ?", salary, user_id)

            return redirect("/transaction")

        # Handle transaction
        if form_type == "transaction":

            category = request.form.get("category")
            amount = request.form.get("amount")
            year = request.form.get("year")
            month = request.form.get("month")
            day = request.form.get("day")
            note = request.form.get("note")

            # If they are null
            if not category or category == "all":
                return apology("must provide category", 400)

            if not amount:
                return apology("must provide amount", 400)

            if not year:
                return apology("must provide year", 400)

            if not month:
                return apology("must provide month", 400)

            if not day:
                return apology("must provide day", 400)

            # Convert the strings to integers
            amount = float(amount)
            year = int(year)
            month = int(month)
            day = int(day)

            # Identify errors
            if amount < 0:
                return apology("amount must be positive", 400)

            if year < 0:
                return apology("year must be positive", 400)

            if month < 1 or month > 12:
                return apology("month must be between 1 and 12", 400)

            if day < 1 or day > 31:
                return apology("day must be between 1 and 31", 400)

            # Insert everything into the table
            db.execute(
                "INSERT INTO transactions (user_id, year, month, day, category, amount, note) " \
                "VALUES(?, ?, ?, ?, ?, ?, ?)",
                user_id, year, month, day, category, amount, note,
            )

            return redirect("/transaction")

        # If form_type is something unexpected
        return apology("invalid form", 400)

    else:

        # Get the user's current salary
        rows = db.execute("SELECT salary FROM users WHERE id = ?", user_id)


        if rows and rows[0]["salary"] is not None:
            salary = rows[0]["salary"]
        else:
            salary = 0

        # Get all the transactions for the user
        transactions = db.execute(
            "SELECT id, year, month, day, category, amount, note FROM transactions WHERE user_id = ? " \
            "ORDER BY year, month, day",
            user_id,
        )

        # Compute current month's totals
        total_expenses_row = db.execute("SELECT SUM(amount) AS total FROM transactions WHERE user_id = ?", user_id)
        total_expenses = total_expenses_row[0]["total"] or 0

        # Calculate savings
        savings = (salary or 0) - total_expenses


        # return template
        return render_template(
            "transactions.html",
            salary=salary,
            transactions=transactions,
            total_expenses=total_expenses,
            savings=savings,
        )


@app.route("/delete_transaction", methods=["POST"])
@login_required
def delete_transaction():
    """Delete a transaction"""

    user_id = session["user_id"]

    # Get the transaction ID to delete
    transaction_id = request.form.get("transaction_id")

    if not transaction_id:
        return apology("must provide transaction ID", 400)

    # Verify the transaction belongs to the user before deleting
    # First check if the transaction exists and belongs to the user
    transaction_check = db.execute(
        "SELECT id FROM transactions WHERE id = ? AND user_id = ?",
        transaction_id, user_id
    )

    if not transaction_check:
        return apology("transaction not found or unauthorized", 400)

    # Delete the transaction
    db.execute(
        "DELETE FROM transactions WHERE id = ? AND user_id = ?",
        transaction_id, user_id
    )

    # Redirect back to transactions page
    return redirect("/transaction")


@app.route("/")
@login_required
def index():
    """ Menu page """
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Identy errors
        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        # Get the user from the database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Identy errors
        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if not confirmation:
            return apology("must provide password confirmation", 400)

        if password != confirmation:
            return apology("password and password confirmation must be the same", 400)

        # Check the unique username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("username taken", 400)

        # Create password hash
        hash = generate_password_hash(password)

        # Insert user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        return redirect("/login")

    else:
        return render_template("register.html")
