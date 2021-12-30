from application import app
from flask import jsonify,make_response,request
from firebase_admin import firestore
from firebase_admin import credentials,initialize_app
import json

import firebase_admin

@app.route("/")
def index():
    return "Welcome to MAYTH server."

@app.route("/posts")
def posts():
    limit = request.args.get('limit')
    page = request.args.get('page')
    responce = get_attraction(int(limit),int(page))
    return jsonify(responce)

@app.route('/', methods=['POST'])
def my_form_post():
    return "Hello post reuqest"


cred = credentials.Certificate("private/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_attraction(limit,page):
    attractions_ref = db.collection(u'attraction')
    attractions = attractions_ref.order_by(u'Title').limit(limit*(page)).stream()
    list = []
    for doc in attractions:
        list.append(doc)
    print(len(list))
    last_doc = list[(-limit)]
    last_pop = last_doc.to_dict()[u'Title']
    print(last_pop)
    next_query = (attractions_ref.order_by(u'Title').start_at({
        u'Title': last_pop
    }).limit(limit)).stream()
    list = []
    for doc in next_query:
        list.append(doc.to_dict())
    return list
