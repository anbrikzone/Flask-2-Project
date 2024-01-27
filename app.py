from flask import Flask, request, render_template, redirect, url_for, flash
from models.employees import Employees

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    employees = Employees()
    ees = employees.get_all_employees()
    context = {
        "title": "Employees",
        "ees": ees,
    }
    return render_template("employees.html", context=context)

@app.route("/form")
def add():
    context = {
        "title": "Employees",
        "user_id": 0,
        "button_name": "Add",
    }
    return render_template("action.html", context=context)

@app.route("/form/<int:user_id>")
def update(user_id):
    context = {
        "title": "Employees",
        "user_id": user_id,
        "button_name": "Update",
    }
    return render_template("action.html", context=context)

@app.route("/remove/<int:user_id>")
def remove(user_id):
    flash("The employee has been removed!")
    return redirect(url_for("index"))
    # employees = Employees()
    # ees = employees.get_all_employees()
    # context = {
    #     "title": "Employees",
    #     "ees": ees,
    # }
    # return render_template("employees.html", context=context)

@app.route("/action", methods=['GET', 'POST'])
def action():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            if user_id != None:
                return redirect(url_for("index"))
        except:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))