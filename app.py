from flask import Flask, request, render_template
from models.employees import Employees

app = Flask(__name__)

@app.route("/")
def index():
    employees = Employees()
    ees = employees.get_all_employees()
    context = {
        "title": "Employees",
        "ees": ees,
    }
    return render_template("employees.html", context=context)

@app.route("/action")
def action():
    context = {
        "title": "Employees",
    }
    return render_template("action.html", context=context)