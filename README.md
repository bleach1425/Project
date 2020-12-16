# Project
聲紋辨識:
1. preprocss.py 為音檔 --> mfcc向量
2. voice_cnn.ipynb --> 為主要的CNN Model
3. American_accent_server.ipynb --> 為後端Server接收音檔並自動轉換為mfcc向量送入模型預測
4. Pika Server、Will Smith | Server等為嘗試明星語音分辨
5. 頻處理測試.ipynb librosa的測試集
(後續新增響度評分、音高頻分、音調評分等還未放入Server)

後端Server:
1. SQL.py --> 某網頁及Unity後端Server
2. Socket_Server.py --> Unity Socket連接
3. Email.py --> 寄信

Model:
Char_RNN.ipynb -->練習RNN預測文字
Neat.ipynb --> Neat練習
fasttext.ipynb --> 文字預測模型(用於聲紋辨識判別語句)

Analysis:
1. 美國大選資料集.ipynb --> Pratice

face recognition
1. face.py --> OpenCV Face Recognition
