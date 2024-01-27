from flask import Flask, request, render_template, redirect, url_for, flash
from models.employees import Employees

app = Flask(__name__)
app.secret_key = '123456'

@app.route("/")
def index():
    employees = Employees().get_all_employees()
    context = {
        "title": "Employees",
        "employees": employees,
    }
    return render_template("employees.html", context=context)

@app.route("/form")
def add():
    context = {
        "title": "Employees",
        "employees": {"user_id": 0, "first_name": "", "last_name": "", "department": "", "salary": ""},
        "button_name": "Add",
    }
    return render_template("action.html", context=context)

@app.route("/form/<int:user_id>")
def update(user_id):
    user_id, first_name, last_name, department, salary = Employees().get_employee_by_id(user_id)
    context = {
        "title": "Employees",
        "employees": {"user_id": user_id, "first_name": first_name, "last_name": last_name, "department": department, "salary": salary},
        "button_name": "Update",
    }
    return render_template("action.html", context=context)

@app.route("/remove/<int:user_id>")
def remove(user_id):
    Employees().remove(user_id)
    flash("The employee has been removed!")
    return redirect(url_for("index"))

@app.route("/action", methods=['GET', 'POST'])
def action():
    if request.method == 'POST':
        first_name = request.form.get(['first_name'], None)
        last_name = request.form.get(['last_name'], None)
        department = request.form.get(['department'], None)
        salary = request.form.get(['salary'], None)
        try:
            user_id = request.form.get(['user_id'], None)
            if user_id != None:
                Employees().update_employee(user_id, first_name, last_name, department, salary)
                return redirect(url_for("index"))
                
        except:
            if first_name != None or last_name !=None or salary != None:
                Employees().create_employee(first_name=first_name, last_name=last_name, department=department, salary=salary)
                return redirect(url_for("index"))
            else:
                return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))