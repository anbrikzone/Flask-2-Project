from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,  nullable=False)
    password = db.Column(db.String,  nullable=False)
    email = db.Column(db.String,  nullable=True)
    tasks = db.relationship("Task", backref="users")

    def __repr__(self):
        return f'<User {self.__tablename__}>'
    
class Task(db.Model):
    
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key = True)
    title  = db.Column(db.String, nullable = False)
    status = db.Column(db.Integer, default = 0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f'<Task {self.__tablename__}>'
    
class Weather(db.Model):
    
    __tablename__ = "weather"
    id = db.Column(db.Integer, primary_key = True)
    location  = db.Column(db.String, nullable = False)
    json  = db.Column(db.String, nullable = False)
    date_update = db.Column(db.String)

    def __repr__(self):
        return f'<Weather {self.location}>'