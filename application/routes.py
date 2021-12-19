from application import app
from flask import request

@app.route("/")
def index():
    return "Hello MAYTH api server."

@app.route('/', methods=['POST'])
def my_form_post():
    return "Hello post reuqest"
