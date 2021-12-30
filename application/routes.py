from application import app
from flask import jsonify,request
from firebase_admin import firestore,storage
from firebase_admin import credentials
from werkzeug.utils import secure_filename
from application.model.attraction import Attraction
import firebase_admin

from application.model.user import User

cred = credentials.Certificate("private/key.json")
firebase_admin.initialize_app(cred,{'storageBucket': "travel-app-12783.appspot.com"})
db = firestore.client()

@app.route("/")
def index():
    return "Welcome to MAYTH server."

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
    attraction = Attraction()
    attraction.db = db
    responce = attraction.get_attraction(int(limit),int(page))
    return jsonify(responce)

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
            return "No images are added..."
    if 'images' in request.files:
        images = request.files.getlist('images')
        index=0
        for i in images:
            images[index].save(secure_filename(i.filename))
            index = index+1
        attraction.images = images
    attraction.title = title
    attraction.district = district
    attraction.latLng = latLng
    attraction.shortDetail = shortDetail
    attraction.youtubeID = youtubeID
    attraction.description = description
    attraction.save_attraction()
    return "Hello post reuqest"
