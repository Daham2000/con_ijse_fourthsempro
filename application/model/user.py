from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from flask import jsonify,make_response
from marshmallow import Schema, fields

class User:
    def __init__(self):
        print("__init__")

    def loginUser(self):
        db = self.db
        users_ref = db.collection(u'users')
        idToken = self.idToken
        loginTime = self.loginTime
        try:
            decoded_token = auth.verify_id_token(idToken)
            email = decoded_token['email']
            data = {
                'lastLogin': loginTime
            }
            new_user_ref = users_ref.document(email)
            new_user_ref.update(data)
            user_doc = new_user_ref.get()
            if user_doc.exists:
                print(f'Document data: {user_doc.to_dict()}')
            else:
                print(u'No such document!')
            return make_response(jsonify(user_doc.to_dict()),200)
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

    def updateUser(self):
        db = self.db
        users_ref = db.collection(u'users')
        email = self.email
        miv = self.miv
        try:
            data = {
                'miv': float(miv)
            }
            new_user_ref = users_ref.document(email)
            new_user_ref.update(data)
            user_doc = new_user_ref.get()
            if user_doc.exists:
                print(f'Document data: {user_doc.to_dict()}')
            else:
                print(u'No such document!')
            return make_response(jsonify(user_doc.to_dict()),200)
        except FirebaseError as e:
            print(e)
            return make_response(jsonify(str("Invalid id token")),401)

class LoginSchema(Schema):
    loginTime = fields.String(required=True)

class UserMIVSchema(Schema):
    miv = fields.Float(required=True)
    email = fields.String(required=True)
