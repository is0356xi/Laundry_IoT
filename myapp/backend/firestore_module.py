import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime


def fire_store():

    dt_now = datetime.datetime.now()

    # Use the application default credentials
    cred = credentials.Certificate("config/laundry-iot-firebase-adminsdk-mdhem-08cc5ef131.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    doc_name = dt_now.strftime('%Y-%m-%d') # 2021-01-10
    query = db.collection('weather').document(doc_name)
    docs = query.get()

    on_time = int(dt_now.strftime('%H'))
    weather_dic = {}
    for k, v in docs.to_dict().items():
        if k[0:2].isdigit() and on_time <= int(k[0:2]):
            weather_dic.update({int(k[0:2]):v})


    weather = sorted(weather_dic.items(), key=lambda x:x[0])
    # print(weather)
    return weather



if __name__=='__main__':
    fire_store()