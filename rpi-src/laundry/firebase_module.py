from google.cloud import storage
from google.cloud import firestore
from google.oauth2 import service_account
import os
import json
from pprint import pprint
import re
import datetime
import time

import subprocess
from subprocess import PIPE


class firebase():
    def __init__(self, client_attr: str):
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

        self.filepath = 'resv_time.txt'
        
        # self.client_storage = storage.Client(
        #     credentials=credentials,
        #     project=credentials.project_id,
        # )
    
        # self.client_store = firestore.Client(
        #     credentials=credentials,
        #     project=credentials.project_id,
        # )

    def bucket_info(self):
        buckets = self.client_storage.list_buckets()
        for obj in buckets:
            print('-------->')
            pprint(vars(obj))
            # get
            bucket = self.client_storage.get_bucket(obj.id)
            print('\t-------->')
            pprint(vars(bucket))

    def get_img(self):
        self.client_storage.read_file("gs://laundry-iot.appspot.com")

    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # source_blob_name = "storage-object-name"
        # destination_file_name = "local/path/to/file"

        bucket = self.client_storage.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        print(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )


    def get_filename(self, bucket_name):
        blobs = self.client_storage.list_blobs(bucket_name)

        name_list = []
        for blob in blobs:
            filename = blob.name
            self._get_time(filename)
            name_list.append(filename)

        return name_list[0]
            

    def _get_time(self, filename):
        content = filename
        pattern = '.*\.'

        # compile後match
        repatter = re.compile(pattern)
        result = repatter.match(content)

        time = result.group()[:-1]

        return time

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
        # ファイルの名前取得
        filename = self.get_filename(bucket_name)
        # Storageから画像を取得する
        self.download_blob(bucket_name, filename, "test.jpg")


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

    def get_reserve_time(self):
        doc_ref = self.client_store.collection(u'reserve').document(u'user1')
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            if data["resv_flag"]:
                resv_time = data["resv_time"]
                self._check_time(resv_time)
            else:
                print("予約キャンセル")
                self._cancel_time()
        else:
            print(u'No such document!')


    def _cancel_time(self):
        proc = subprocess.run("./delete_atjob.sh", shell=True, stdout=PIPE, stderr=PIPE, text=True)
        output = proc.stdout
        print(output)



    def _check_time(self, resv_time):
        from datetime import datetime as dt

        now = time.strftime('%Y-%m-%d %H:%M')

        if os.path.isfile(self.filepath):
            with open(self.filepath) as f:
                pref_time = f.read()
                print("前の予約時間 => {}".format(pref_time))

                dt_time = dt.strptime(resv_time, '%Y-%m-%d %H:%M')
                dt_pref = dt.strptime(pref_time, '%Y-%m-%d %H:%M')
                dt_now = dt.strptime(now, '%Y-%m-%d %H:%M')

                if dt_time == dt_pref:
                    print("時間変更なし")
                elif dt_time < dt_now:
                    print("現在時刻より前")
                else:
                    print("予約時間が変更されました")
                    self._cancel_time()
                    self._set_time(resv_time)
                    print("{0} --> {1}".format(pref_time, resv_time))
        else:
            self._set_time(resv_time)
            

    def _set_time(self, resv_time):
        new_date, new_time = resv_time.split()

        year = new_date.split("-")[0]
        month = new_date.split("-")[1]
        day = new_date.split("-")[2]

        at_time = new_time
        at_date = month + day + year

        proc = subprocess.run("./atjob_set.sh {0} {1}".format(at_time, at_date), shell=True, stdout=PIPE, stderr=PIPE, text=True)
        output = proc.stdout
        print(output)

        with open(self.filepath, mode='w') as f:
                f.write(resv_time)



       





def main():
    client_attr = "store"
    # client_attr = "storage"
    fb = firebase(client_attr)
    fb.get_reserve_time()
    # fb.get_img()



if __name__ == "__main__":
    main()
    