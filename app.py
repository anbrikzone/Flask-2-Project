from flask import Flask, request, conte, render_template

app = Flask(__name__)

@app.route("/")
def index():
    context = {
        "title": "List of Employees",
    }
    return render_template("employees.html", context=context)