from application import app
from flask import jsonify,request
from firebase_admin import firestore,storage
from firebase_admin import credentials
from werkzeug.utils import secure_filename

import firebase_admin

cred = credentials.Certificate("private/key.json")
firebase_admin.initialize_app(cred,{'storageBucket': "travel-app-12783.appspot.com"})
db = firestore.client()

@app.route("/")
def index():
    return "Welcome to MAYTH server."

@app.route("/posts")
def posts():
    limit = request.args.get('limit')
    page = request.args.get('page')
    attraction = Attraction()
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

class Attraction:
    def __init__(self):
        print("")
    
    def get_attraction(self,limit,page):
        attractions_ref = db.collection(u'attraction')
        attractions = attractions_ref.order_by(u'Title').limit(limit*(page)).stream()
        list = []
        for doc in attractions:
            list.append(doc)
        last_doc = list[(-limit)]
        last_pop = last_doc.to_dict()[u'Title']
        next_query = (attractions_ref.order_by(u'Title').start_at({
            u'Title': last_pop
        }).limit(limit)).stream()
        list = []
        for doc in next_query:
            list.append(doc.to_dict())
        return list
    
    def save_attraction(self):
        attractions_ref = db.collection(u'attraction')
        images = []
        for i in self.images:  
            fileName = i.filename
            print(fileName)
            bucket = storage.bucket()
            blob = bucket.blob(fileName)
            blob.upload_from_filename(fileName)
            blob.make_public()
            images.append(blob.public_url)
            print("your file url", blob.public_url)

        data = {
        'Description': self.description,
        'District': self.district,
        'ShortDetail': self.shortDetail,
        'Title': self.title,
        'youtubeID': self.youtubeID,
        'LatLng': self.latLng,
        'Images': images,
        }
        responce = attractions_ref.document(self.title).set(data)
        print(responce)
        return responce