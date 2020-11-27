from flask import Flask, request, abort
import scraping_server
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
Otenki = scraping_server.Otenki()

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/index", methods=['POST'])
def index():
    return 'OK'

def get_weather(rain_flag=True, today_flag=True):
    # 1時間ごとの天気予報を取得
    tenki_list = Otenki.get_weather(today_flag)

    # 何時かをカウントする
    count = 0

    # 雨情報を保持する辞書
    rain = {}
    # 晴れ情報を保持する辞書
    sunny = {}

    # 雨 or 晴れを見つける
    for tenki in tenki_list:
        if tenki == "晴れ":
            sunny[count] = tenki
        elif tenki != "曇り":
            rain[count] = tenki
        else:
            print("曇り")

        count += 1

    # app.logger.info("get_weather: {0} ||| {1}".format(rain, sunny))
    print("rain: {0} ||| sunny: {1}".format(rain, sunny))

    # 雨を返すか晴れを返すか
    if rain_flag:
        return rain
    else:
        return sunny
        

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザからのメッセージ
    user_msg = event.message.text
  
    # 返信
    if user_msg == "雨予報":
        # 雨が降るかどうか取得して返信
        rain = get_weather(True)
        msg = Otenki.weather_reply(rain, True)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
    elif user_msg == "晴れ予報":
        # 晴れるかどうか取得して返信
        sunny = get_weather(False)
        print(sunny)
        msg = Otenki.weather_reply(sunny, False)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
    
    elif user_msg == "明日の雨予報":
        # 雨が降るかどうか取得して返信
        rain_flag = True
        today_flag = False
        rain = get_weather(rain_flag ,today_flag)
        msg = Otenki.weather_reply(rain, True)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="'雨予報' or '晴れ予報' or '明日の雨予報'を送ってこいよ"))




if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)