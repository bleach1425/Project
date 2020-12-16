# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import pandas as pd
from datetime import datetime


already_list=[]
already = pd.read_json('XXX.json', encoding='utf-8')
for n in already.iloc:
    already_list.append(n['captcha'])

def send_email():
    with open("Account.json", mode="r", encoding="utf-8") as f:
        info = json.load(f)
        user_data = pd.read_json("User_Data.json", encoding="utf-8")
        mail_target = [n for i, n in enumerate(user_data.iloc) if n['captcha'] not in already_list]
        ## save point
        name_list=[]
        email_list=[]
        identity_list=[]
        captcha_list=[]

        for i, mail in enumerate(mail_target):
            ## data
            name = mail['account']
            email = mail['email']
            identity = mail['identity']
            captcha = mail['captcha']
            ## save to list
            name_list.append(name)
            email_list.append(email)
            identity_list.append(identity)
            captcha_list.append(captcha)

            print("----------------------------")
            print("正在寄送給寄送給:", name, '....')
            print(name, email, identity)

            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(info['account'], info['password'])
            print("由",info['account'],"寄出....")
            from_addr = info["account"]
            to_addr = email

            Subject = "XXX"

            message = MIMEMultipart()
            message['From'] = from_addr
            message['To'] = to_addr
            message['Subject'] = Subject

            if identity == "V" or identity == "P":
                message.attach(MIMEText(name + (info["msg1"].format(mail['captcha']))))
            elif identity == "NO":
                message.attach(MIMEText(name + (info['msg2'].format(mail['captcha']))))
            else:
                message.attach(MIMEText(name + (info['msg'].format(mail['captcha']))))
            status = smtp.sendmail(from_addr, to_addr, message.as_string()) # 加密文件，避免私密信息被截取
            if status=={}:
                print("郵件傳送成功!")
                print("----------------------------")
                print(" ")
            else:
                print("郵件傳送失敗!")
                print("----------------------------")
                print(" ")
            smtp.quit()
            mail_dict={
                "account":name_list,
                "email":email_list,
                "identity":identity_list,
                "captcha":captcha_list
            }
            save_csv = pd.DataFrame(mail_dict)
            New_time = datetime.now().strftime('%m%d')
            save_csv.to_csv(f"已經寄送的名單/{New_time}寄送名單.csv", encoding='big5',index=False)
            return "Email Sent"


if __name__ == '__main__':
    send_email()
