from copy import Error
from firebase_admin import storage
from firebase_admin.exceptions import FirebaseError
from flask import jsonify,make_response

class Attraction:
    def __init__(self):
        print("__init__")
    
    def get_attraction(self,limit,page):
        db = self.db
        query = self.query
        attractions_ref = db.collection(u'attraction')
        try:
            totalPosts = attractions_ref.order_by('Title').stream()
            if query==None:
                attractions = attractions_ref.order_by('Title').limit(limit*(page)).stream()
            elif query=="":
                attractions = attractions_ref.order_by('Title').limit(limit*(page)).stream()
            else:
                query = query.strip()
                try:
                    attractions = attractions_ref.where("Title", ">=", query).limit(limit*(page)).stream()
                except FirebaseError as e:
                    return make_response(jsonify(str(e)),422)
            list = []
            for doc in attractions:
                list.append(doc)
            totalItems = len(list)
            totalNeeded = limit*(page-1)
            # get total posts number
            posts = []
            for doc in totalPosts:
                posts.append(doc)
            numOfTotalPosts = len(posts)
            
            if totalItems>totalNeeded:
                difference = totalItems-totalNeeded
                print(difference)
                if difference<limit:
                    last_doc = list[(-difference)]
                else:    
                    last_doc = list[(-limit)]
                list = []
                last_pop = last_doc.to_dict()['Title']
                next_query = (attractions_ref.order_by('Title').start_at({
                    'Title': last_pop
                }).limit(limit)).stream()
                for doc in next_query:
                    list.append(doc.to_dict())
            else:
                list = []
            return make_response(jsonify({"totalItems":numOfTotalPosts,"posts":list}),200)
            
        except Error as e:
            return make_response(jsonify(str(e)),422)
    
    def save_attraction(self):
        db = self.db
        attractions_ref = db.collection(u'attraction')
        images = []
        for i in self.images:  
            fileName = i.filename
            print(fileName)
            bucket = storage.bucket()
            blob = bucket.blob(fileName)
            blob.upload_from_file(i)
            blob.make_public()
            images.append(blob.public_url)
            print("your file url", blob.public_url)
        
        try:
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
        except FirebaseError as e:
            return make_response(jsonify(str(e)),422)

        return make_response(jsonify(str("Post created...")),201)