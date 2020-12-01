import json
import pandas as pd


        # for n in range(len(user_data['account'])):
        # name = user_data["account"][n]
        # print("----------------------------")
        # print("正在寄送給寄送給:", name, '....')
        # email = user_data["email"][n]
        # identity = user_data["identity"][n]
        # print(name, email, identity)
#     for n in range(len(data['account'])):
#         print('--------------------------------')
#         print("名字: ",data['account'][n])
#         print("信箱: ", data['email'][n])
#         print("身份: ", data['identity'][n])
#         print('--------------------------------')
#         print('')
# import pandas as pd
# import paddlehub as hub
# import jieba
# data = pd.read_excel("Apple.xlsx")
# for n in range(1,32):
#     data = data.drop([f"Unnamed: {n}"], axis=1)
# data.columns=["使用者評論"]
#
# jieba.set_dictionary('jieba_dict.txt')
# def cut_funtion(row):
#     row = str(row)
#     dot = [',' , '+', '-', '*', '/', '!', '...'
#            '?' , '， ', '']
#     for dots in dot:
#         row.strip(dots)
#     cut_text = jieba.cut(row)
#     word = " ".join(cut_text)
#     return word
#
#
# from senta import Senta
#
# my_senta = Senta()
#
# # 选择是否使用gpu
# use_cuda = False # 设置True or False
#
# # 预测中文句子级情感分类任务
# my_senta.init_model(model_class="ernie_1.0_skep_large_ch", task="sentiment_classify", use_cuda=use_cuda)
# texts = ["中山大学是岭南第一学府"]
# result = my_senta.predict(texts)
# print(result)
#
# my_senta.init_model(model_class="ernie_1.0_skep_large_ch", task="aspect_sentiment_classify", use_cuda=use_cuda)
# texts = ["百度是一家高科技公司"]
# aspects = ["百度"]
# result1 = my_senta.predict(texts, aspects)
# print(result1)

# import threading
# import time
#
# t1 = time.time()
#
# def first_job(n):
#     print("thread %s is running..." % threading.current_thread().name)
#     print("這是第一個程式")
#
# def two_job(n):
#     print("這是第二個程式")
#
# def three_job(n):
#     print("這是第三個程式")
#
#
# Initial_value1= 1
# Initial_value2 = 2
# Initial_value3 = 3
#
#
# class Muti():
#     def __init__(self, name):
#         self.name = name
#     def main(self):
#         global Initial_value1, Initial_value2, Initial_value3
#         for i, n in enumerate(range(10000)):
#             try:
#                 if (i+1) % 3 == 1:
#                     print(i)
#                     one = threading.Thread(target=first_job(n))
#                     print("---------------------------")
#                     one.start()
#                     print("---------------------------")
#
#                 elif (i+1) % 3 == 2:
#                     print(i)
#                     two = threading.Thread(target=two_job(n))
#                     print("---------------------------")
#                     two.start()
#                     print("---------------------------")
#                 else:
#                     print(i)
#                     three = threading.Thread(target=three_job(n))
#                     print("---------------------------")
#                     three.start()
#                     print("---------------------------")
#             except:
#                 print("Done")
#                 print(threading.active_count())
#         print("Done")
#         t2 = time.time()
#         cost_time = round((t2-t1),2)
#         print(cost_time)
#
# Unity = Muti("Unity")
# print(Unity.main())
#
#
# # def email_send(email_, identity_, account_):
# #     global db, cursor
# #     with open("Account.json", mode="r", encoding='utf-8') as f:
# #         data = json.load(f)
# #         # sender_data
# #         SENDER = 'yinglijob268@gmail.com'
# #         SENDERNAME = '穎利科研'
# #         # you want sent mail target
# #         RECIPIENT = email_
# #         # AWS user_account
# #         USERNAME_SMTP = "AKIAVF7XD7CKKZESCBAU"
# #         PASSWORD_SMTP = "BA+Rm6AmS7fDHi4PoN3Nzrxd3CiRWt6rQir3EsQGS/0j"
# #         # Set
# #         CONFIGURATION_SET = "Only_test"
# #         HOST = "email-smtp.ap-northeast-1.amazonaws.com"
# #         PORT = 587
# #
# #         # The subject line of the email.
# #         SUBJECT = '中華物聯網與人共智慧國際大會'
# #         # print(identity_)
# #         # The email body for recipients with non-HTML email clients.
# #         if identity_ == "V":
# #             BODY_TEXT = (
# #                 account_ + data["msg1"]
# #             )
# #         elif identity_ == "NO":
# #             BODY_TEXT=(
# #                 account_ + data["msg2"]
# #             )
# #         else:
# #             BODY_TEXT = (
# #                 account_ + data["msg"]
# #             )
# #
# #         msg = MIMEMultipart('alternative')
# #         msg['Subject'] = SUBJECT
# #         msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
# #         msg['To'] = RECIPIENT
# #         # Comment or delete the next line if you are not using a configuration set
# #         msg.add_header('X-SES-CONFIGURATION-SET', CONFIGURATION_SET)
# #
# #         # Record the MIME types of both parts - text/plain and text/html.
# #         part1 = MIMEText(BODY_TEXT, 'plain')
# #         part1.encoding="utf-8"
# #         msg.attach(part1)
# #
# #         try:
# #             server = smtplib.SMTP(HOST, PORT)
# #             server.ehlo()
# #             server.starttls()
# #             server.ehlo()
# #             server.login(USERNAME_SMTP, PASSWORD_SMTP)
# #             server.sendmail(SENDER, RECIPIENT, msg.as_string())
# #             server.close()
# #         # Display an error message if something goes wrong.
# #         except Exception as e:
# #             print("Error: ", e)
# #         else:
# #             print("Email sent!")
# #         return "OK"
#
#
#
#
