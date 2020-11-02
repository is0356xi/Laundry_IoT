import requests
from bs4 import BeautifulSoup

class Otenki:
    # インスタンス作成時に1度だけHTTPリクエストを送る
    def __init__(self):
        #tenki.jpのページのURL(滋賀県草津市)
        url = 'https://tenki.jp/forecast/6/28/6010/25206/1hour.html'

        #HTTPリクエスト
        r = requests.get(url)

        # BoutifulSoupオブジェクトの生成
        self.bsObj = BeautifulSoup(r.content, "html.parser")


    def get_chance_rain(self):
        # 1h毎の降水確率を取得してリストに格納
        today_1h = self.bsObj.find(class_="forecast-point-1h")
        prob_rain_1h = today_1h.find(class_="prob-precip")
        proc_list = prob_rain_1h.find_all("td")

        # 確率の値を格納するリスト
        proc_value_list = []

        # 値を抽出
        for i in proc_list:
            value = i.find("span").string
        if value != "---" : #現在時刻より前は"---"となるので-1に変換
            proc_value_list.append(i.find("span").string)
        else:
            proc_value_list.append(-1)

        return proc_value_list

    def get_weather(self):
        # 1h毎の天気予報を取得してリストに格納
        today_1h = self.bsObj.find(class_="forecast-point-1h")
        weather_1h = today_1h.find(class_="weather")
        weather_list = weather_1h.find_all("td")

        # 天気予報の値を格納するリスト
        weather_value_list = []

        # 値の格納
        for i in weather_list:
            value = i.p.string
            weather_value_list.append(value)

        return weather_value_list