from firebase_admin import firestore,storage
db = ''

class Attraction:
    def __init__(self):
        print("__init__")
    
    def get_attraction(self,limit,page):
        db = self.db
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
        db = self.db
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