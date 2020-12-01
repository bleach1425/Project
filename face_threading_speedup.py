# -*- coding: utf-8 -*-
import cv2
import time
import threading
import face_recognition as fb


# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False

        # 攝影機連接。
        self.capture = cv2.VideoCapture(URL)

    def start(self):
        # 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        # 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('ipcam stopped!')

    def getframe(self):
        # 當有需要影像時，再回傳最新的影像。
        return self.Frame

    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()

        self.capture.release()


URL = "rtsp://admin:admin@192.168.1.1/video.h264"

# 連接攝影機
ipcam = ipcamCapture(0)
cap = cv2.VideoCapture(0)
# 啟動子執行緒
ipcam.start()

# 暫停1秒，確保影像已經填充
time.sleep(1)

# 使用無窮迴圈擷取影像，直到按下Esc鍵結束
while True:
    # 使用 getframe 取得最新的影像
    I = ipcam.getframe()
    ret, frame = cap.read()
    rgb_frame = frame[:, :, ::-1]
    # Find all the faces in the current frame of video
    face_locations = fb.face_locations(rgb_frame)
    print(face_locations)
    for top, right, bottom, left in face_locations:
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0,
                                                            255), 2)
    cv2.imshow('Video', frame)
    if cv2.waitKey(2) == 27:
        cv2.destroyAllWindows()
        fb.face_locations()
        ipcam.stop()
        break