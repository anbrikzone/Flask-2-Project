from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import session
from models.basemodel import User, Task, Weather, db
from services.weatherapi import WeatherAPI
from services.geolocationapi import LocationAPI
from datetime import datetime, timedelta
import json
import os



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = "123456"
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir + '/database', 'db.sqlite')

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

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
            "user": ""
        }
        return render_template("login.html", context=context)
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("tasks"))
        else:
            return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        context = {
            "title": "To-Do List"
        }
        return render_template("register.html", context=context)
    elif request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password == confirm_password:
            user = User(username=username, password=generate_password_hash(password), email=email)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("tasks"))
        else:
            flash("'Password' and 'Confirm Password' are not equal!")
            return redirect(url_for("register"))

@app.route("/remove/<int:id>")
@login_required
def remove(id):
    Task.query.filter_by(id = id).delete()
    db.session.commit()
    flash("The task has been removed!")
    return redirect(url_for("tasks"))

@app.route("/done/<int:id>")
@login_required
def done(id):
    task = Task.query.filter_by(id = id).update({"status": 1})
    db.session.commit()
    return redirect(url_for("tasks"))

@app.route("/tasks", methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        task_title = request.form.get('task_title')
        user_id = request.form.get('user_id')
        if task_title.strip() != "":
            task = Task(title=task_title, status=0, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for("tasks"))
        else:
            return redirect(url_for("tasks"))
    elif request.method == 'GET':
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.status.asc(), Task.id.desc()).all()
        
        # This block defines city of user (by default set Atyrau)
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")
        else:
            ip = request.remote_addr
        city = "Atyrau" if ip == "127.0.0.1" else LocationAPI().get_location(ip)['city']
        
        weather = Weather.query.filter_by(location=city).first()
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
    
@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))