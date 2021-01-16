const btnSubscribe = document.getElementById('btnSubscribe');
const btnUnSubscribe = document.getElementById('btnUnSubscribe');
const textInstanceIdToken = document.getElementById('textInstanceIdToken');
const sendWebPushArea = document.getElementById('sendWebPushArea');
const sendWebPush = document.getElementById('sendWebPush');

// メッセージング オブジェクトの取得
const messaging = firebase.messaging();

// アプリにウェブ認証情報を設定する
messaging.usePublicVapidKey("BAT6wt0K0FejA2mL_WCERg4G0orJIFFA7pFAI9GbOTz_EIMf8T5uX45AD62Vjg3tliWyJ62f2tCaol3wnP2UxIE");


function postToken(token) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '../api/token');
    xhr.setRequestHeader('Content-Type', 'application/json');

    // 受信に成功したとき
    xhr.onload = function () {
        let result = JSON.parse(xhr.responseText);
        console.log(result);
        if(result == "401") {
            alert("トークン登録エラー：ログイン状態を確認してください")
        } else if (result == "400") {
            alert("トークン登録エラー：サーバ側でエラーが発生しました")
        }
    };

    // XMLHttpRequestを送信
    xhr.send(JSON.stringify({token: token}));
}


// 権限要求
function requestPermission() {
    // 通知を受信する権限を要求する
    messaging.requestPermission().then(function() {
        // 現在の登録トークンの取得
        messaging.getToken().then(function(token) {
            postToken(token);
            textInstanceIdToken.value =  token;
            btnSubscribe.style.display = 'none';
            btnUnSubscribe.style.display = 'block';
            sendWebPushArea.style.display = 'block';
            // sendWebPush.value = 'http://localhost:8080/notify_test?id=' + token;
        }).catch(function(err) {
            textInstanceIdToken.value = 'トークンの取得に失敗しました（' + err + '）。';
        });
    }).catch(function(err) {
        textInstanceIdToken.value = '通知の許可が得られませんでした（' + err + '）。';
    });
}

// トークン削除
function deleteToken() {
    // トークン取得
    messaging.getToken().then(function(currentToken) {
        // トークン削除
        messaging.deleteToken(currentToken).then(function() {
            textInstanceIdToken.value = 'トークンが削除されました';
            btnSubscribe.style.display = 'block';
            btnUnSubscribe.style.display = 'none';
            sendWebPushArea.style.display = 'none';
            sendWebPush.value = '';
        }).catch(function(err) {
            textInstanceIdToken.value = 'トークンの削除に失敗しました（' + err + '）。';
        });
    }).catch(function(err) {
        textInstanceIdToken.value = 'トークンの取得に失敗しました（' + err + '）。';
    });
}

// 初期化
window.onload = function() {
    // イベント登録
    btnSubscribe.onclick = requestPermission;
    btnUnSubscribe.onclick = deleteToken;
    // トークン取得
    messaging.getToken().then(function(currentToken) {
        if (currentToken) {
            // 本来ここでサーバにトークン送る処理
            postToken(currentToken);
            //sendTokenToServer(currentToken);
            textInstanceIdToken.value = currentToken;
            btnSubscribe.style.display = 'none';
            btnUnSubscribe.style.display = 'block';
            sendWebPushArea.style.display = 'block';
            sendWebPush.value = 'http://localhost:8080/notify_test?id=' + token;
        } else {
            // トークン無い場合
            textInstanceIdToken.value = '通知の許可をしていません。「通知を許可する」を押してください。';
        }
    }).catch(function(err) {
        textInstanceIdToken.value = 'トークンの取得に失敗しました（' + err + '）。';
    });
};