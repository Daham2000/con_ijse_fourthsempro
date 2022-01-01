from application import app
from flask import jsonify,request,make_response
from firebase_admin import firestore,storage
from firebase_admin import credentials
from werkzeug.utils import secure_filename
from application.model.attraction import Attraction
import firebase_admin
from marshmallow import Schema, fields, ValidationError

from application.model.user import LoginSchema, User

cred = credentials.Certificate("private/key.json")
firebase_admin.initialize_app(cred,{'storageBucket': "travel-app-12783.appspot.com"})
db = firestore.client()

@app.route("/")
def index():
    return "Welcome to MAYTH server."

@app.route("/auth/login", methods=['GET'])
def login():
    request_data = request.args
    schema = LoginSchema()
    try:
        result = schema.load(request_data)
        loginTime = request_data.get('loginTime')
    except ValidationError as err:
        return jsonify(err.messages), 400    
    user = User()
    user.db = db
    user.loginTime = loginTime
    bearer = request.headers.get('Authorization')
    token = bearer.split()[1] 
    user.idToken = token
    res = user.loginUser()
    return res

@app.route("/users/register", methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    user = User()
    user.db = db
    user.email = email
    user.password = password
    user.firstName = firstName
    user.lastName = lastName
    res = user.registerUser()
    return res

@app.route("/posts")
def posts():
    limit = request.args.get('limit')
    page = request.args.get('page')
    query = request.args.get('query')
    attraction = Attraction()
    attraction.db = db
    attraction.query = query
    responce = attraction.get_attraction(int(limit),int(page))
    return responce

@app.route('/admin/post', methods=['POST'])
def my_form_post():
    title = request.form['title']
    district = request.form['district']
    latLng = request.form.getlist('latLng')
    shortDetail = request.form['shortDetail']
    youtubeID = request.form['youtubeID']
    description = request.form['description']
    attraction = Attraction()
    attraction.db = db
    if 'images' not in request.files:
            return make_response("Images field can't be empty...",404)
    images = request.files.getlist('images')
    attraction.images = images
    attraction.title = title
    attraction.district = district
    attraction.latLng = latLng
    attraction.shortDetail = shortDetail
    attraction.youtubeID = youtubeID
    attraction.description = description
    res = attraction.save_attraction()
    return res
