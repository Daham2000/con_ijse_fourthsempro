from application import application
from flask import jsonify,request,make_response
from firebase_admin import firestore
from firebase_admin import credentials
from werkzeug.utils import secure_filename
from application.model.attraction import Attraction
import firebase_admin
from marshmallow import ValidationError
from application.model.hotel import Hotel

from application.model.user import LoginSchema, User, UserMIVSchema
from application.mi_model.predict_model import make_prediction

cred = credentials.Certificate("private/key.json")
firebase_admin.initialize_app(cred,{'storageBucket': "travel-app-12783.appspot.com"})
db = firestore.client()

@application.route("/")
def index():
    return "Welcome to MAYTH server."

@application.route("/predict")
def predict():
    predict = make_prediction(10000,4)
    return predict

@application.route("/auth/login", methods=['GET'])
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

@application.route("/user/miv", methods=['PATCH'])
def updateMivUser():
    request_data = request.form
    schema = UserMIVSchema()
    try:
        schema.load(request_data)
        email = request.form['email']
        miv = request.form['miv']
    except ValidationError as err:
        return jsonify(err.messages), 400    
    user = User()
    user.db = db
    user.email = email
    user.miv = miv
    res = user.updateUser()
    return res

@application.route("/users/register", methods=['POST'])
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

@application.route("/posts")
def posts():
    limit = request.args.get('limit')
    page = request.args.get('page')
    query = request.args.get('query')
    attraction = Attraction()
    attraction.db = db
    attraction.query = query
    responce = attraction.get_attraction(int(limit),int(page))
    return responce

@application.route("/hotels")
def hotels():
    limit = request.args.get('limit')
    page = request.args.get('page')
    query = request.args.get('query')
    hotel = Hotel()
    hotel.db = db
    hotel.query = query
    responce = hotel.get_hotels(int(limit),int(page))
    return responce

@application.route('/admin/post', methods=['POST'])
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

@application.route('/admin/hotel', methods=['POST'])
def add_hotel():
    title = request.form['title']
    district = request.form['district']
    link = request.form['link']
    description = request.form['description']
    miv = request.form['miv']
    rate = request.form['rate']
    hotel = Hotel()
    hotel.db = db
    hotel.rate = rate
    hotel.miv = miv
    if 'images' not in request.files:
            return make_response("Images field can't be empty...",404)
    images = request.files.getlist('images')
    hotel.images = images
    hotel.title = title
    hotel.district = district
    hotel.link = link
    hotel.description = description
    res = hotel.save_hotel()
    return res
