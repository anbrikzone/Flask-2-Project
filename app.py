from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.basemodel import User, Task, Weather, db
from services.weatherapi import WeatherAPI
from services.geolocationapi import LocationAPI
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = "e694f80ee6729b0d521d064384da7ecd"
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir + '/database', 'db.sqlite')

# Setup for login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Initialize db
db.init_app(app)
with app.app_context():
    db.create_all()

# Return User object if that exist in db
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Index route
@app.route("/")
def index():
    context = {
        "title": "To-Do List"
    }
    return render_template("index.html", context=context)

# login user route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        context = {
            "title": "To-Do List",
            "user": ""
        }
        return render_template("login.html", context=context)
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Use ORM to obtain user object
        user = User.query.filter_by(username = username).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("tasks"))
        else:
            return redirect(url_for("login"))

# Register user route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        context = {
            "title": "To-Do List",
            "user": ""
        }
        return render_template("register.html", context=context)
    elif request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # if password and confirm password are equal then add new user (with hash of password) in db
        if password == confirm_password:
            user = User(username=username, password=generate_password_hash(password), email=email)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("tasks"))
        else:
            flash("'Password' and 'Confirm Password' are not equal!")
            return redirect(url_for("register"))

# Remove task route
@app.route("/remove/<int:id>")
@login_required
def remove(id):
    Task.query.filter_by(id = id).delete()
    db.session.commit()
    flash("The task has been removed!")
    return redirect(url_for("tasks"))

# Done task route
@app.route("/done/<int:id>")
@login_required
def done(id):
    task = Task.query.filter_by(id = id).update({"status": 1})
    db.session.commit()
    return redirect(url_for("tasks"))

# Tasks route
@app.route("/tasks", methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        task_title = request.form.get('task_title')
        user_id = request.form.get('user_id')
        
        # if task field is not empty add new task
        if task_title.strip() != "":
            task = Task(title=task_title, status=0, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for("tasks"))
        else:
            return redirect(url_for("tasks"))
    elif request.method == 'GET':
        # Get all tasks by user id and order them by status and id 
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.status.asc(), Task.id.desc()).all()
        
        # This block defines city of user by IP address (by default is set Atyrau)
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")
        else:
            ip = request.remote_addr
        city = "Atyrau" if ip == "127.0.0.1" else LocationAPI().get_location(ip)['city']
        
        weather = Weather.query.filter_by(location=city).first()
        
        # This block is allow to store data about weather in db and check/update it every 2 hours
        if weather is not None:
            if datetime.strptime(weather.date_update,"%Y-%m-%d %H:%M:%S") >= datetime.now() - timedelta(hours=2):
                weather_json = json.loads(weather.json.replace("'", '"'))
            else:
                weather_json = WeatherAPI().get_weather(city)
                Weather.query.filter_by(location = city).update({"json": str(weather_json), "date_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                db.session.commit()
        else:
            weather_json = WeatherAPI().get_weather(city)
            weather = Weather(location = city, json = str(weather_json), date_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(weather)
            db.session.commit()

        context = {
            "title": "Tasks",
            "user": current_user.username,
            "user_id": current_user.id,
            "tasks": tasks,
            "weather": weather_json["current"]['temp_c']
        }
        return render_template("tasks.html", context=context)

# Logout route
@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))