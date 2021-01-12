import cv2
import time
import numpy as np
import os
import subprocess
import datetime

class cam_func:
    def __init__(self, size=(224, 224)):
        # 色々初期化
        self.cap = cv2.VideoCapture(0)
        self.size = size
        self.count = 0
        self.preflame = None
        self.prefbboxes = None 
        self.prefoverlap = -1
        self.upload_flag = False
        self.pref_call_time = None
        self.pref_update = None
        
        # 背景画像を設定する
        self._set_backgroud()

        
    def _set_backgroud(self):
        # self.background = self._get_frame()
        self.background = cv2.imread("background.jpg", 0)
        print("背景画像を設定したよ")
        


    def update_background(self):
        img = self._get_frame()
        cv2.imwrite("background.jpg",img)
        self._set_backgroud()
        self.count = 0
        print("背景画像をアップデーティッド")
        

    def _get_frame(self, blur_flag=False):
        # フレームの取得
        _, frame = self.cap.read()
        # 画像のリサイズ
        frame = cv2.resize(frame, self.size)
        # frame = frame[:, self.x1:self.x2, :].astype("uint8")
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # 画像の平滑化(ぼかし)
        blur = cv2.GaussianBlur(frame, (5,5), 0)
        # blur = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)

        if blur_flag:
            return frame, blur
        else:
            return frame


    def test_show(self, bg, fr, fgmask):
        while True:
            cv2.imshow("background", bg)
            cv2.imshow("frontground", fr)
            cv2.imshow("fgmask", fgmask)
            #エンターキーでブレイク
            k = cv2.waitKey(1)
            if k == 13:
                self.cap_release()
                cv2.destroyAllWindows()
                break
    

    def cap_release(self):
        #カメラを解放するだけの関数
        self.cap.release()

        
    def detection(self):
        # while True:
        #     if self.preflame is None:
        #         self.preflame = self._get_frame()

        # 背景アップデートを判定するカウント
        i=0

        while True:
            # frontフレームの取得
            frame = self._get_frame()
            # 背景差分
            mask = self._get_background_subtraction(frame, self.background)
            # 物体検出
            frame = self._get_bbox(mask, frame)

            self.now = time.time()

            # アップロードする画像を更新する
            self._update_frontground()

            i += 1

            time.sleep(0.06)
            # 一定時間経過したら背景画像を更新
            if(i > 1000):
                self.update_background()
                i=0
        
            cv2.imshow("Frame", frame)
            cv2.imshow("Background", self.background)
            cv2.imshow("mask", mask)

            k = cv2.waitKey(1)
            if k == 13:
                self.cap_release()
                cv2.destroyAllWindows()
                break
            

    def _get_bbox(self, mask, frame):
        
        # 輪郭抽出
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        # 小さい輪郭は除く
        contours = list(filter(lambda x: cv2.contourArea(x) > 250, contours))

        # 輪郭を囲む外接矩形を取得
        bboxes = list(map(lambda x: cv2.boundingRect(x), contours))

        # 重複している物体を検出
        bboxes = self._get_IoU(bboxes)

        # 矩形を描画
        if bboxes is not None:
            for x, y, w, h in bboxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame
       

    def _get_IoU(self, bboxes):
        # 何回検出したら物体と判定するかの回数
        object_count = 60
        # 同じような物体を検出するために前フレームで検出した物体を保持
        if self.prefbboxes is None:
            self.prefbboxes = bboxes
            return bboxes


        # 同じような物体を検出
        return_bboxes = []

        for bbox in bboxes:
            for prefbbox in self.prefbboxes:
                overlap = self.iou(bbox, prefbbox)
                
                # 同じような物体を検出した時
                if overlap > 0.99:
                    return_bboxes.append(bbox)
                    if overlap == self.prefoverlap:
                        self.count += 1
                    else:
                        pass

                    if self.count >= object_count:
                        print("detected!!!")
                        self.count = 0
                        # 検出時間を更新するかどうかのチェック
                        self.upload_check()

                self.prefoverlap = overlap
                

        self.prefbboxes = bboxes

        return return_bboxes


    def upload_check(self):
        # アップロードチェックが呼び出された時間
        call_time = time.time()

        # 初回呼び出し or 前回呼び出された時間と比較して時間が十分経過しているかチェック
        if self.pref_call_time is None or self.time_check(self.pref_call_time, call_time):
            self.upload_flag = not self.upload_flag
            print(self.upload_flag)


        self.pref_call_time = call_time

    def _update_frontground(self):
        now = datetime.datetime.now()
        update_time = time.time()
        if self.upload_flag:
            # 時間経過が十分な場合に画像を更新
            if self.pref_update is None  or update_time - self.pref_update > 60:
                filename = 'images/' + now.strftime('%Y-%m-%d_%H:%M:%S') + '.jpg'
                img = self._get_frame()
                cv2.imwrite(filename,img)
                self.pref_update = update_time
        else:
            # if os.path.exists('images/upload.jpg'):
            #     subprocess.call('rm -rf images/upload.jpg', shell=True)
            pass

    def time_check(self, time1, time2):
        print(time2-time1)
        if time2-time1 > 60:
            return True
        else:
            return False



    def iou(self, a: tuple, b: tuple) -> float:
        a_x1, a_y1, a_x2, a_y2 = a
        b_x1, b_y1, b_x2, b_y2 = b
        
        if a == b:
            score = 1.0
        elif (
            (a_x1 <= b_x1 and a_x2 > b_x1) or (a_x1 >= b_x1 and b_x2 > a_x1)
        ) and (
            (a_y1 <= b_y1 and a_y2 > b_y1) or (a_y1 >= b_y1 and b_y2 > a_y1)
        ):
            intersection = (min(a_x2, b_x2) - max(a_x1, b_x1)) * (min(a_y2, b_y2) - max(a_y1, b_y1))
            union = (a_x2 - a_x1) * (a_y2 - a_y1) + (b_x2 - b_x1) * (b_y2 - b_y1) - intersection
            score = intersection / union
        else:
            score = 0.0

        return score



    def _get_background_subtraction(self, front, bg):
        th = 30    # 差分画像の閾値

        # 差分をとる
        mask = cv2.absdiff(front, bg)

        # 二値化する
        mask[mask < th] = 0
        mask[mask >= th] = 255

        # メディアンフィルタ処理（ゴマ塩ノイズ除去）
        mask = cv2.medianBlur(mask, 3)

        return mask




def main():
    cam = cam_func()
    cam.update_background()

    # while True:
    #     cam.detection()
    
    cam.detection()
    cam.test_mask()

if __name__ == "__main__":
    main()