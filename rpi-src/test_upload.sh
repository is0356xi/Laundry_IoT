export PATH=${PATH}:$HOME/gsutil
gsutil -o 'Credentials:gs_service_key_file=/home/pi/firebase_admin.json' cp /home/pi/Laundry_IoT/rpi-src/camera/background.jpg gs://laundry-iot.appspot.com/
