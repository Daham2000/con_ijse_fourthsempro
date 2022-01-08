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
            }
            responce = attractions_ref.document(self.title).set(data)
        except FirebaseError as e:
            return make_response(jsonify(str(e)),422)

        return make_response(jsonify(str(responce)),201)