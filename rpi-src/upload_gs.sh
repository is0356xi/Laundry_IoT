#!/bin/bash

export PATH=${PATH}:$HOME/gsutil

TARGET_DIR="/home/pi/Laundry_IoT/rpi-src/camera/images"

cd $TARGET_DIR

# ファイルの存在確認を行い、あればアップロードする
while :
do
	if [ -n "$(ls)" ]; then
		file=`ls`
		echo $file
		gsutil -o 'Credentials:gs_service_key_file=/home/pi/firebase_admin.json' cp "${TARGET_DIR}/${file}" gs://laundry-iot.appspot.com/user1/

		rm -rf $file
	else
		echo "file not exists."
	fi

	sleep 10
done