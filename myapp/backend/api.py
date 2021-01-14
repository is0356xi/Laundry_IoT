from flask import Blueprint, request, session
from flask_restful import Api, Resource, reqparse
import firebase_module

api_bp = Blueprint('api', __name__, url_prefix='/api')
parser = reqparse.RequestParser()
parser.add_argument('time')
parser.add_argument('mail')
parser.add_argument('password')

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
        # return status_code
        return status_code

class Signin(Resource):
    def post(self):
        data = parser.parse_args()
        mail_address = data["mail"]
        password = data["password"]
        # print(mail_address, password)
        fb = firebase_module.firebase("store")
        status_code, doc_id = fb.signin(mail_address, password)
        # return status_code
        session['usr'] = doc_id
        print(session)
        
        return status_code

api = Api(api_bp)
api.add_resource(Spam, '/spam')
api.add_resource(Weather, '/weather')
api.add_resource(Reserve, '/reserve')
api.add_resource(Cancel, '/cancel')
api.add_resource(Signin, '/signin')