from flask import Flask, request, abort
import scraping_server
import os


Otenki = scraping_server.Otenki()

def weather_reply(data_dic, rain_flag):
    # 天気情報が空じゃない場合
    if len(data_dic) >= 1:
        time_list = list(data_dic.keys())

        # 連続した時間をまとめる (ex. 1,2,3時 --> 1~3時)
        msg_list = []
        prev_time = -1
        for time in time_list:
            if prev_time - time == 1:
                start = time
            else:
                end = time
                msg = "{0}時~{1}時".format(start, end) 
                msg_list.append(msg)

            prev_time = time

        return str(msg_list)
    # 天気情報が空だった場合
    else:
        if rain_flag:
            text = "雨は降らないぜよ"
        else:
            text = "晴れないぜよ"

        return text

if __name__ == "__main__":
    