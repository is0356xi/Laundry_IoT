import requests
from bs4 import BeautifulSoup

class Otenki:
    # インスタンス作成時に1度だけHTTPリクエストを送る
    def __init__(self):
        #tenki.jpのページのURL(滋賀県草津市)
        url = 'https://tenki.jp/forecast/6/28/6010/25206/1hour.html'

        # ヘッダーを設定
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5)" "AppleWebKit/537.36 (KHTML, like Gecko) Chrome", "Accept": "text/html,application/xhtml+xml,application/xml;" "q=0.9,image/webp,image/apng,*/*;q=0.8"}

        #HTTPリクエストを送る
        get_data = requests.get(url)

        # BoutifulSoupオブジェクトの生成
        self.bsObj = BeautifulSoup(get_data.content, "html.parser")


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

    def get_weather(self, today_flag=True):
        if today_flag:
            # 1h毎の天気予報を取得してリストに格納
            today_1h = self.bsObj.find(id="forecast-point-1h-today")
            weather_1h = today_1h.find(class_="weather")
            weather_list = weather_1h.find_all("td")
        else:
            # 1h毎の天気予報を取得してリストに格納
            tomorrow_1h = self.bsObj.find(id="forecast-point-1h-tomorrow")
            weather_1h = tomorrow_1h.find(class_="weather")
            weather_list = weather_1h.find_all("td")

        # 天気予報の値を格納するリスト
        weather_value_list = []

        # 値の格納
        for i in weather_list:
            value = i.p.string
            weather_value_list.append(value)

        return weather_value_list

    def weather_reply(self, data_dic, rain_flag):
        # 天気情報が空じゃない場合
        if len(data_dic) >= 1:
            time_list = list(data_dic.keys())

            # 連続した時間をまとめる (ex. 1,2,3時 --> 1~3時)
            msg_list = []
            start = time_list[0]
            end = 0
            last_time = time_list[0]

            for time in time_list:

                # 連続している時
                if time - last_time <= 1:
                    end = time
                # 連続していない時
                else:
                    if end - start != 0:
                        msg = "{0}時~{1}時".format(start, end)
                    else:
                        msg = "{0}時".format(end)

                    msg_list.append(msg)
                    
                    start = time
                    end = time

                # 一個前の時間を更新
                last_time = time
            
            if start == end:
                msg_list.append("{0}時".format(end))
            else:
                msg_list.append("{0}時~{1}時".format(start, end))

            return str(msg_list)

        # 天気情報が空だった場合
        else:
            if rain_flag:
                text = "雨は降らないぜよ"
            else:
                text = "晴れないぜよ"

            return text


if __name__ == "__main__":
    Otenki = Otenki()
    sunny = {1: '晴れ', 2: '晴れ', 3: '晴れ', 5: '晴れ', 6: '晴れ', 7: '晴れ', 9: '晴れ', 10: '晴れ', 11: '晴れ', 12: '晴れ', 13: '晴れ', 14: '晴れ', 15: '晴れ', 16: '晴れ', 17: '晴れ', 18: '晴れ', 19: '晴れ'}
    msg = Otenki.weather_reply(sunny, False)
    print(msg)