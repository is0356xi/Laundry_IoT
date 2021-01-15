from flask import Blueprint, request, session
from flask_restful import Api, Resource, reqparse
import firebase_module

api_bp = Blueprint('api', __name__, url_prefix='/api')
parser = reqparse.RequestParser()
parser.add_argument('time')
parser.add_argument('mail')
parser.add_argument('password')
parser.add_argument('name')

class Spam(Resource):
    def get(self):
        return [{'id': 42, 'name': 'Name', 'note': 'Note'}]

class Weather(Resource):
    def get(self):
        fb = firebase_module.firebase("store")
        weathers = fb.get_weather()
        return weathers

class Reserve(Resource):
    def post(self):
        data = parser.parse_args()
        resv_time = data["time"]
        fb = firebase_module.firebase("store")
        status_code = fb.reserve(resv_time)
        # return status_code
        return data, status_code

class Cancel(Resource):
    def get(self):
        fb = firebase_module.firebase("store")
        status_code = fb.cancel()
        # return status_code∂
        return status_code

class Img(Resource):
    def get(self):
        fb = firebase_module.firebase("storage")
        status_code = fb.get_img()
        # return status_code
        return status_code

class Signin(Resource):
    def post(self):
        data = parser.parse_args()
        mail_address = data["mail"]
        password = data["password"]
        fb = firebase_module.firebase("store")
        status_code = fb.signin(mail_address, password)

        return status_code

class Signup(Resource):
    def post(self):
        data = parser.parse_args()
        mail = data["mail"]
        password = data["password"]
        name = data["name"]
        fb = firebase_module.firebase("store")
        status_code = fb.signup(mail, password, name)

        return status_code

class Islogin(Resource):
    def get(self):
        if session.get('usr'):
            if session['usr']:
                return 'ok'
            else:
                return 'ng'
        else:
            return 'ng'


class Logout(Resource):
    def get(self):
        try:
            del session['usr']
            return 201
        except:
            return 400



api = Api(api_bp)
api.add_resource(Spam, '/spam')
api.add_resource(Weather, '/weather')
api.add_resource(Reserve, '/reserve')
api.add_resource(Cancel, '/cancel')
api.add_resource(Img, '/img')
api.add_resource(Signin, '/signin')
api.add_resource(Signup, '/signup')
api.add_resource(Islogin, '/islogin')
api.add_resource(Logout, '/logout')
