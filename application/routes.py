from application import app
from flask import jsonify,make_response
from firebase_admin import firestore
from firebase_admin import credentials,initialize_app
import json

import firebase_admin

@app.route("/")
def index():
    j = get_attraction()
    return make_response(jsonify(j), 200)

@app.route('/', methods=['POST'])
def my_form_post():
    return "Hello post reuqest"


cred = credentials.Certificate("private/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

attractions = db.collection(u'attraction').stream()

print(attractions)

def get_attraction():
    for doc in attractions:
        print(type(doc.to_dict()))
    return "attractions"
