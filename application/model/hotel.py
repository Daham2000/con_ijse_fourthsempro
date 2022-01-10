from copy import Error
from firebase_admin import storage
from firebase_admin.exceptions import FirebaseError
from flask import jsonify,make_response

class Hotel:
    def __init__(self):
        print("__init__")

    def save_hotel(self):
        db = self.db
        attractions_ref = db.collection(u'hotels')
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
                'description': self.description,
                'district': self.district,
                'title': self.title,
                'link': self.link,
                'Images': images,
                'rate': int(self.rate),
                'miv': float(self.miv),
            }
            responce = attractions_ref.document(self.title).set(data)
            doc_ref = db.collection("hotels").document(self.title)
            doc = doc_ref.get().to_dict()
        except FirebaseError as e:
            return make_response(jsonify(str(e)),422)

        return make_response(jsonify(doc),201)

    def get_hotels(self,limit,page):
        db = self.db
        query = self.query
        hotels_ref = db.collection(u'hotels')
        try:
            totalPosts = hotels_ref.order_by('title').stream()
            if query==None:
                hotels = hotels_ref.order_by('title').limit(limit*(page)).stream()
            elif query=="":
                hotels = hotels_ref.order_by('title').limit(limit*(page)).stream()
            else:
                query = query.strip()
                try:
                    hotels = hotels_ref.where("miv", "==", float(query)).limit(limit*(page)).stream()
                except FirebaseError as e:
                    return make_response(jsonify(str(e)),422)
            list = []
            for doc in hotels:
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
                last_pop = last_doc.to_dict()['title']
                next_query = (hotels_ref.order_by('title').start_at({
                    'title': last_pop
                }).limit(limit)).stream()
                for doc in next_query:
                    list.append(doc.to_dict())
            else:
                list = []
            return make_response(jsonify({"totalItems":numOfTotalPosts,"hotels":list}),200)
            
        except Error as e:
            return make_response(jsonify(str(e)),422)