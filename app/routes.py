from flask import request, render_template
from app import app


@app.route('/', methods=['GET'])
def index():
    return "PARTY TIME BOYZZZZ"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.jinja2')
