from application import app
from flask import request
from firebase_admin import firestore
from firebase_admin import credentials,initialize_app

import firebase_admin

@app.route("/")
def index():
    return "Hello MAYTH api server."

@app.route('/', methods=['POST'])
def my_form_post():
    return "Hello post reuqest"


cred = credentials.Certificate("private/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()