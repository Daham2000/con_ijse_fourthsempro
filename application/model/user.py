from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from flask import jsonify,make_response

class User:
    def __init__(self):
        print("__init__")

    def loginUser(self):
        db = self.db
        idToken = self.idToken
        loginTime = self.loginTime
        try:
            decoded_token = auth.verify_id_token(idToken)
            uid = decoded_token['uid']
            print(uid)
            return make_response(jsonify(uid),200)
        except FirebaseError as e:
            print(e)
            return make_response(jsonify(str("Invalid id token")),401)

    def registerUser(self):
        db = self.db
        users_ref = db.collection(u'users')
        firstName = self.firstName
        lastName = self.lastName
        email = self.email
        password = self.password

        try:
            user = auth.create_user(
                email=email,
                email_verified=False,
                password=password,
                display_name=firstName,
                disabled=False)
            print('Sucessfully created new user: {0}'.format(user.uid))
        except FirebaseError as e:
            print(e)
            return make_response(jsonify(str(e)),409)
        
        try:
            data = {
            'email': email,
            'firstName': firstName,
            'lastName': lastName,
            'uid': user.uid
            }
            users_ref.document(self.email).set(data)
            
            new_user_ref = users_ref.document(email)

            user_doc = new_user_ref.get()
            if user_doc.exists:
                print(f'Document data: {user_doc.to_dict()}')
            else:
                print(u'No such document!')
            r = []
            r.append(user_doc.to_dict())
        except FirebaseError as e:
            return make_response(jsonify(str(e)),422)
            
        return make_response(jsonify(r),201)
