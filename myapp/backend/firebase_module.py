from google.cloud import storage
from google.cloud import firestore
from google.oauth2 import service_account
import os
import json
from pprint import pprint
import re
import datetime

from flask import session


class firebase():
    def __init__(self, client_attr: str):
        """
        params
            client_attr: ストレージにアクセスするか・ストアにアクセスするか => "storage" or "store"
        """

        key_path = os.path.join(os.path.join(os.environ['HOME'], 'firebase_admin.json'))
        service_account_info = json.load(open(key_path))
        credentials = service_account.Credentials.from_service_account_info(service_account_info)

        if client_attr == "storage":
            self.client_storage = storage.Client(
                credentials=credentials,
                project=credentials.project_id,
            )
        elif client_attr == "store":
            self.client_store = firestore.Client(
                credentials=credentials,
                project=credentials.project_id,
            )

        try:
            self.user_id = session["usr"]
        except:
            self.user_id = "user1"

        
    def bucket_info(self):
        buckets = self.client_storage.list_buckets()
        for obj in buckets:
            print('-------->')
            pprint(vars(obj))
            # get
            bucket = self.client_storage.get_bucket(obj.id)
            print('\t-------->')
            pprint(vars(bucket))


    def get_filename(self, bucket_name):
        blobs = self.client_storage.list_blobs(bucket_name)

        name_list = []
        for blob in blobs:
            filename = blob.name
            name_list.append(filename)

        
        target_filename = self._get_latest(name_list)

        return target_filename
            

    def _get_latest(self, name_list: list) -> str:
        target_files = []
        for filename in name_list:
            # ファイル名からuser_idを取得
            user_id = filename.split("/")[0]
            # user_idが含まれるファイルだけ取得
            if self.user_id == user_id:
                target_files.append(filename)
                print(filename)
            else:
                pass

        print(target_files)
        return target_files[0]

            # content = filename
            # pattern = '.*\.'

            # # compile後match
            # repatter = re.compile(pattern)
            # result = repatter.match(content)

            # time = result.group()[:-1]

            # return time

    def get_weather(self):

        dt_now = datetime.datetime.now()

        doc_name = dt_now.strftime('%Y-%m-%d') # 2021-01-10
        query = self.client_store.collection('weather').document(doc_name)
        docs = query.get()

        on_time = int(dt_now.strftime('%H'))
        weather_dic = {}
        for k, v in docs.to_dict().items():
            if k[0:2].isdigit() and on_time <= int(k[0:2]):
                weather_dic.update({int(k[0:2]):v})


        weather = sorted(weather_dic.items(), key=lambda x:x[0])
        # print(weather)
        return weather


    def get_img(self):
        bucket_name = "laundry-iot.appspot.com"

        dst_name = "../frontend/public/static/img/test.jpg"
        # Storageから画像を取得する
        status_code = self.download_blob(bucket_name, dst_name)

        return status_code

    def download_blob(self, bucket_name, destination_file_name):
        """Downloads a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # source_blob_name = "storage-object-name"
        # destination_file_name = "local/path/to/file"

        try:
            # バケットのアクセス
            bucket = self.client_storage.bucket(bucket_name)

            # ダウンロードするファイル名を取得
            source_blob_name = self.get_filename(bucket_name)

            # ファイルをダウンロード
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)

            print(
                "Blob {} downloaded to {}.".format(
                    source_blob_name, destination_file_name
                )
            )
            return 201
        except Exception as err:
            print(err)
            return 401
            


    def reserve(self, time):
        resv_time = time

        try:
            doc_ref = self.client_store.collection(u'reserve').document(u'user1')
            doc_ref.set({
                u'resv_time': time,
                u'resv_flag': True
            })
            return 201
        except Exception as e:
            print(e)
            return 400


    def cancel(self):
        try:
            doc_ref = self.client_store.collection(u'reserve').document(u'user1')
            doc_ref.set({
                u'resv_flag': False
            })
            return 201
        except Exception as e:
            print(e)
            return 400




def main():
    # client_attr = "store"
    client_attr = "storage"
    user_id = "user1"
    fb = firebase(client_attr, user_id)
    # fb.get_weather()
    fb.get_img()
    # fb.download_blob()

    

    

if __name__ == "__main__":
    main()
    