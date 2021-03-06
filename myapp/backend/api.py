from flask import Blueprint, request, session
from flask_restful import Api, Resource, reqparse
import firebase_module

api_bp = Blueprint('api', __name__, url_prefix='/api')

parser = reqparse.RequestParser()
parser.add_argument('time')
parser.add_argument('mail')
parser.add_argument('password')
parser.add_argument('name')
parser.add_argument('token')

class Spam(Resource):
    def get(self):
        return [{'id': 42, 'name': 'Name', 'note': 'Note'}]

class Weather(Resource):
    def get(self):
        fb = firebase_module.firebase("store")
        table = True
        weathers = fb.get_weather(table)
        return weathers

class Reserve(Resource):
    def post(self):
        data = parser.parse_args()
        resv_time = data["time"]
        
        fb = firebase_module.firebase("store")
        data = fb.reserve(resv_time)
        print(data)
        # return status_code
        return data

class Cancel(Resource):
    def get(self):
        fb = firebase_module.firebase("store")
        status_code = fb.cancel()
        # return status_code∂
        return status_code

class Img(Resource):
    def get(self):
        fb = firebase_module.firebase("storage")
        status_code = fb.get_images()
        # return status_code
        return status_code

class Signin(Resource):
    def post(self):
        data = parser.parse_args()
        mail_address = data["mail"]
        password = data["password"]
        fb = firebase_module.firebase("store")
        message, status_code = fb.signin(mail_address, password)

        return {'message': message, 'status_code': status_code}

class Signup(Resource):
    def post(self):
        data = parser.parse_args()
        mail = data["mail"]
        password = data["password"]
        name = data["name"]
        fb = firebase_module.firebase("store")

        result, status_code = fb.checkUserName(name)

        if status_code == 201:
            if result == 'used':
                return {'message': 'The username is already in use', 'status_code': status_code}
            elif result == 'not used':
                message, status_code = fb.signup(mail, password, name)
                return {'message': message, 'status_code': status_code}
        else:
            return {'message': result, 'status_code': status_code}

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


class Token(Resource):
    def post(self):
        if(not session.get('usr')):
            return 401
        data = parser.parse_args()
        token = data["token"]
        fb = firebase_module.firebase("store")
        status_code = fb.updateToken(token)

        return status_code


class Check(Resource):
    def get(self):
        fb = firebase_module.firebase("store")
        data = fb.check_resv()

        return data


class WeatherToday(Resource):
    def get(self):
        fb = firebase_module.firebase("store")
        weathers = fb.get_today_weather()
        return weathers


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
api.add_resource(Token, '/token')
api.add_resource(Check, '/check_resv')
api.add_resource(WeatherToday, '/weather_today')
