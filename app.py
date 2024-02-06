from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager
from models.users import Users
from models.tasks import Tasks
from models.weather import Weather
from services.weatherapi import WeatherAPI
from services.geolocationapi import LocationAPI
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = '123456'

@app.route("/")
def index():
    context = {
        "title": "To-Do List"
    }
    return render_template("index.html", context=context)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        context = {
            "title": "To-Do List",
            "user": 0
        }
        return render_template("login.html", context=context)
    elif request.method == "POST":
        
        return render_template("login.html", context=context)

@app.route("/register", methods=["GET", "POST"])
def register():
    context = {
        "title": "To-Do List"
    }
    return render_template("register.html", context=context)

# @app.route("/form")
# def add():
#     context = {
#         "title": "Tasks",
#         "tasks": {"id": 0, "title": "", "status": "", "user_id": 0},
#         "button_name": "Add",
#     }
#     return render_template("action.html", context=context)

# @app.route("/form/<int:user_id>")
# def update(user_id):
#     user_id, first_name, last_name, department, salary = Employees().get_employee_by_id(user_id)
#     if str(salary).split(".")[1] == "0":
#         salary = int(salary)
#     context = {
#         "title": "Employees",
#         "employees": {"user_id": user_id, "first_name": first_name, "last_name": last_name, "department": department, "salary": salary},
#         "button_name": "Update",
#     }
#     return render_template("action.html", context=context)

@app.route("/remove/<int:id>")
def remove(id):
    Tasks().remove(id)
    flash("The task has been removed!")
    return redirect(url_for("index"))

@app.route("/done/<int:id>")
def done(id):
    Tasks().done(id, 1)
    return redirect(url_for("index"))

@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    print("test")
    if request.method == 'POST':
        task_title = request.form['task_title']
        user_id = request.form['user_id']
        if task_title.strip() != "":
            Tasks().create(title=task_title, status=0, user_id=user_id)
            return redirect(url_for("index"))
        else:
            return redirect(url_for("index"))
    elif request.method == 'GET':
        tasks = Tasks().get_all(1)
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")
        else:
            ip = request.remote_addr
        city = "Atyrau" if ip == "127.0.0.1" else LocationAPI().get_location(ip)
        weather = Weather().get_by_location(city)
        if weather is not None:
            if datetime.strptime(weather[0],"%Y-%m-%d %H:%M:%S") >= datetime.now() - timedelta(hours=2):
                weather_json = json.loads(weather[1].replace("'", '"'))
            else:
                weather_json = WeatherAPI().get_weather("Atyrau")
                Weather().update("Atyrau", str(weather_json))
        else:
            weather_json = WeatherAPI().get_weather("Atyrau")
            Weather().create(location = "Atyrau", json = str(weather_json), date_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        context = {
            "title": "Tasks",
            "tasks": tasks,
            "weather": weather_json["current"]['temp_c']
        }
        return render_template("tasks.html", context=context)