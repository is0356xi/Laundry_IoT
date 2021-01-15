from flask import Flask, render_template, request, send_file
from api import api_bp
import os
import requests
import pprint
import json

# app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist', static_url_path='/')
app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')
app.register_blueprint(api_bp)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/token/<path:path>')
def token(path):
    return send_file('./token/' + path)

@app.route('/firebase-messaging-sw.js')
def fb_sw():
    return send_file('./token/firebase-messaging-sw.js')

@app.route('/notify_test')
def ntest():
    if request.args.get('id') is not None:
        query = request.args.get('id')
    else:
        query = "Token Error!"
        return query

    json_msg = {"notification":{
                "title": "通知のタイトル",
                "body": "通知の本文",
                "icon": "http://www.ritsumei.ac.jp/image.jsp?id=294173",
                "click_action": "https://www.google.com/"
            },
            "to": query}

    response = requests.post('https://fcm.googleapis.com/fcm/send',
        json.dumps(json_msg),
        headers={'Content-Type': 'application/json',
                'Authorization': 'key=AAAAZULDIrs:APA91bGo7sIyQOQOqFe8ZvWt7d9apWToWa7W6s3CuLmRXSP1iM-atbDLGSskUGPYe5M3qPxp95SpPyp2zpaqTiJBQtUsMSFeFGue80a0w4YcQZ-IWWOm7AcyEQ78DifJlQW72bsI6AL3'})
    pprint.pprint(response.json())

    return response.json()

if __name__ == '__main__':
    app.run()
    # app.run(debug=False, host='0.0.0.0', port=48080)