self.addEventListener("notificationclick", function(event) {
    const notificationData = event.notification.data.FCM_MSG.notification;
    const title = notificationData.title;
    const body = notificationData.body;
    const clickAction = notificationData.click_action;
    event.notification.close();
    event.waitUntil(
        clients.openWindow(clickAction)
    );
});

importScripts('https://www.gstatic.com/firebasejs/8.2.2/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.2.2/firebase-messaging.js');

firebase.initializeApp({
    'apiKey': "AIzaSyAvimkk_Q5xj9zZiXiasT8OUylQrKYn2R0",
    'authDomain': "laundry-iot.firebaseapp.com",
    'projectId': "laundry-iot",
    'storageBucket': "laundry-iot.appspot.com",
    'messagingSenderId': "434911781563",
    'appId': "1:434911781563:web:902d16e361849fc993ff9e",
    'measurementId': "G-6S5GR5S094"
});

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload) {
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: payload.notification.icon
    };
    console.log(payload.notification.body);
    console.log(payload.notification.icon);
    return self.registration.showNotification(notificationTitle, notificationOptions);
});
