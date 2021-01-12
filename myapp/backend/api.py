from flask import Blueprint
from flask_restful import Api, Resource
import firebase_module

api_bp = Blueprint('api', __name__, url_prefix='/api')

class Spam(Resource):
    def get(self):
        return [{'id': 42, 'name': 'Name', 'note': 'Note'}]

class Weather(Resource):
    def get(self):
        fb = firebase_module.firebase("store")
        weathers = fb.get_weather()
        return weathers

api = Api(api_bp)
api.add_resource(Spam, '/spam')
api.add_resource(Weather, '/weather')