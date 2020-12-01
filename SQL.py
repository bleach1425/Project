#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
from flask import Flask, jsonify, request, render_template
from flask_cors import cross_origin
from datetime import datetime
from random import Random
import json
import gc

app = Flask(__name__)
json_data=""
json_list = []
dict_={"playerDatas":json_list}

account_list=[]
email_list=[]
identity_list=[]
captcha_list=[]

columns = ["ID", "Cellphone", "account", "captcha", "email", "identity", "job", "unit", "isOnline", "uid"]
# db_link
db = MySQLdb.connect("127.0.0.1", "lili", "lili", "Award_Data" ,charset="utf8")
cursor = db.cursor()
db.ping(True)
# cursor.execute(sql)


def check_unity_online():
    with open("User_Online.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
        response = data["Playlist"]
        return {"playlist": response}

## 刪除資料!!
def add_unity_online(cellphone_, account_, captcha_,job_ ,identity_, email_, unit_, uid_, isOnline_):
    with open("User_Online.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
        if len(data["Playlist"]) == 1:
            print('有一人離開會議室')
            if data["Playlist"][0]["Cellphone"] == cellphone_:
                print(data["Playlist"][0]["account"], " 已離開伺服器")
                data=None
            with open("User_Online.json", mode="w", encoding="utf-8") as f:
                json.dump(data, f)
                return "OK"

        else:
            print('有多人離開會議室')
            for i, n in enumerate(data["Playlist"]):

                if data["Playlist"][i]["Cellphone"] == cellphone_:
                    print(data["Playlist"][i]["account"]," 已離開伺服器")
                    del data["Playlist"][i]

                with open("User_Online.json", mode="w", encoding="utf-8") as f:
                    json.dump(data, f)
            return "OK"


def add_identity_code(cellphone_, identity_, account_, email_, unit_, job_, captcha_):
    global db, cursor
    # print(cellphone_, identity_)
    sql = f"UPDATE `test` SET `identity`='{identity_}', `captcha`='{captcha_}' WHERE `Cellphone`= '{cellphone_}'"
    # print(sql)
    data = cursor.execute(sql)
    db.commit()
    return {"status":"currect" , "message":"Update Currect"}


## fix
def invite_acount(account_, email_, cellphone_, unit_, job_, english_):
    global db, cursor
    sql = f"SELECT * FROM `test` WHERE `Cellphone` = {cellphone_}"
    data = cursor.execute(sql)
    datetime_ = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if data == 0:
        sql = f"INSERT INTO `test`(`Cellphone`, `account`, `captcha`, `email`, `identity`, `job`, `unit`, `isOnline`, `uid`, `english`, `datetime`) VALUES ('{cellphone_}', '{account_}', 'captcha', '{email_}', 'identity', '{job_}',  '{unit_}', 'False', 'uid', '{english_}', '{datetime_}')"
        data = cursor.execute(sql)
        data_dict={
            "status":"correct",
            "account":account_,
            "email":email_,
            "cellphone":cellphone_,
            "english":english_,
            "datetime":datetime_
        }
        db.commit()
        return data_dict
    elif data != 0:
        return {"status":"error", "message":"申請的電話已重複"}

def check(cellphone_,name_):
    global db, cursor
    try:
        sql = f"SELECT * FROM `test` WHERE `Cellphone` = {cellphone_}"
        data = cursor.execute(sql)
        name = data[0][1]
        check_response = data[0]
        if name == name_:
            return {'check_response':check_response}
        else:
            return {"status" : "error", "message" : "name error"}
    except:
        return {"status":"error", "message":"Not registered"}

## unity content
def save_message_sql(AgendaIndex_, SubtitleIndex_, PPTIndex_, AgendaPPTIndex):
    global db, cursor
    sql = f"UPDATE `content` SET `content` = '{AgendaIndex_}', `Subtitleindex` = '{SubtitleIndex_}', `PPTindex` = '{PPTIndex_}', `AgendaPPTIndex` = '{AgendaPPTIndex}' WHERE `ID` = '1'"
    # print(sql)
    cursor.execute(sql)
    db.commit()
    return "OK"

## return untiy_content
def show_message_sql():
    global db, cursor
    sql = "SELECT * FROM `content`"
    sql_out = cursor.execute(sql)
    data = cursor.fetchall()

    data_dict={
        "AgendaIndex":data[0][1],
        "SubtitleIndex":data[0][2],
        "PPTIndex":data[0][3],
        "AgendaPPTIndex":data[0][4]
    }
    final = json.dumps(data_dict)
    return final

def set_uid(id_, cellphone_, account_, captcha_, identity_, email_, job_, unit_, uid_, isOnline_):
    with open("User_Online.json", mode="r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if len(data["Playlist"]) >= 1 or data["Playlist"] == None:
                # print("2")
                New_data = {
                    "ID":id_,
                    "Cellphone":cellphone_,
                    "account":account_,
                    "captcha":captcha_,
                    "identity":identity_,
                    "email":email_,
                    "job":job_,
                    "unit":unit_,
                    "uid":uid_,
                    "isOnline":isOnline_
                }
                data["Playlist"].append(New_data)
                # print(data)
                with open("User_Online.json", mode="w", encoding="utf-8") as f:
                    json.dump(data, f)
                    return "OK"
        except:
            # print("3")
            data = {
                "ID":id_,
                "Cellphone":cellphone_,
                "account":account_,
                "captcha":captcha_,
                "identity":identity_,
                "email":email_,
                "job":job_,
                "unit":unit_,
                "uid":uid_,
                "isOnline":isOnline_
            }
            data_list=[data]
            New_data = {"Playlist":data_list}
            print(New_data)
            print(len(New_data))
            with open("User_Online.json", mode="w", encoding="utf-8") as f:
                json.dump(New_data, f)
                return "OK"

# CORS(app) unity login
@app.route('/Award/login', methods=['GET', "POST"])
@cross_origin()
def make_account():
    # Get url
    user_data = request.get_json()
    account_ = user_data['name']
    email_ = user_data['email']
    cellphone_ = user_data['cellphone']
    unit_ = user_data['unit']
    job_ = user_data['job']
    english_ = user_data['english']
    add = invite_acount(account_, email_, cellphone_, unit_, job_, english_)
    # print("add",add)
    return add

## check your account repeat
@app.route('/Award/check', methods=['GET', "POST"])
@cross_origin()
def check_account():
    user_data = request.get_json()
    cellphone_ = user_data['cellphone']
    name_ = user_data['name']
    check_value = check(cellphone_,name_)
    return check_value

## Catch All_Data , Check unity numbers of people
@app.route('/Award/unity', methods=["POST", "GET"])
@cross_origin()
def unity_sever():
    data = request.get_json()
    cellphone_ = data['Cellphone']
    print(cellphone_)
    account_ = data['account']
    captcha_ = data['captcha']
    identity_ = data['identity']
    email_ = data['email']
    job_ = data['job']
    unit_ = data['unit']
    uid_ = data['uid']
    isOnline_ = data['isOnline']
    # -------------------------------------------------------#

    add = add_unity_online(cellphone_, account_, captcha_, job_, identity_, email_, unit_, uid_, isOnline_)
    return add

##  Add uid!!
@app.route('/Award/unity/set_uid', methods=["POST", "GET"])
@cross_origin()
def unity_first_set():
    # data
    data = request.get_json()
    id_ = data["ID"]
    cellphone_ = data['Cellphone']
    account_ = data['account']
    captcha_ = data['captcha']
    identity_ = data['identity']
    email_ = data['email']
    job_ = data['job']
    unit_ = data['unit']
    # print(id_, cellphone_, account_, captcha_, identity_, email_, job_, unit_)
    uid_ = data['uid']
    isOnline_ = data['isOnline']
    # response
    response = set_uid(id_, cellphone_, account_, captcha_, identity_, email_, job_, unit_, uid_, isOnline_)
    return response

## unity要全部的資料,
@app.route('/unity/content', methods=["POST", "GET"])
@cross_origin()
def unity_sever_content():
    global dict_
    data = request.get_json()
    # print("新增使用者: ",data)
    dict_['playerDatas'].append(data)
    # print("dict_",dict_)
    return {"status":"currect"}


@app.route('/unity/content/get', methods=["POST", "GET"])
@cross_origin()
def unity_get_safe():
    global dict_, json_data
    if dict_ == {}:
        return ""
    else:
        json_data = json.dumps(dict_)
        # print("json_data: ",json_data)
        return json_data

## unity_request  response: All Data
@app.route('/Award/All_Data', methods=["POST", "GET"])
@cross_origin()
def check_User():
    global db, cursor, columns
    sql = "SELECT * FROM `test`"
    data = cursor.execute(sql)
    data = cursor.fetchall()
    # print(data)
    response = {
        "response":data
    }
    json_response = json.dumps(response)
    # print(json_response)
    return json_response


## fix
@app.route('/Award/Add_Data', methods=["POST", "GET"])
@cross_origin()
def add_identity():
    global name_list, email_list, identity_list, captcha_list
    random = Random()
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    captcha_ = ""
    length = len(chars) - 1
    for i in range(7):
        captcha_+=chars[random.randint(0, length)]
    data = request.get_json()
    # Add Data
    cellphone_ = data['cellphone']
    identity_ = data['identity']
    account_ = data['account']
    email_ = data['email']
    unit_ = data['unit']
    job_ = data['job']
    captcha_ = identity_+captcha_
    response = add_identity_code(cellphone_, identity_, account_, email_, unit_, job_, captcha_)

    with open("User_Data.json", mode="w" ,encoding="utf-8") as f:
        User_dict={
            "account":account_list,
            "email":email_list,
            "identity":identity_list,
            "captcha":captcha_list
        }
        User_dict["account"].append(account_)
        User_dict["email"].append(email_)
        User_dict["identity"].append(identity_)
        User_dict['captcha'].append(captcha_)
        User_Info = json.dump(User_dict, f)
        print("save data currect !!")

    return response


# searchCaptcha
@app.route('/Award/Captcha', methods=["POST", "GET"])
@cross_origin()
def search_email():
    captcha_ = request.args['captcha']
    global db, cursor, columns
    # part 1
    sql=f"SELECT * FROM `test` WHERE `captcha` = '{captcha_}'"
    data_unm = cursor.execute(sql)
    if data_unm == 0:
        return {'status': "error", "message": "驗證碼錯誤"}
    data = cursor.fetchall()
    Data_list = []
    if data[0][3] == captcha_:
        target = dict(zip(columns, list(data[0])))
        return { "rowUserInfo" : target }

@app.route('/Award/check_online', methods=["POST", "GET"])
@cross_origin()
def check_online():
    response = check_unity_online()
    # print("3")
    # print(response)
    return response

@app.route('/Award/save_message', methods=["POST", "GET"])
@cross_origin()
def save_message():
    data = request.get_json()
    # print(data)
    Agendaindex_ = data['AgendaIndex']
    Subtitleindex_ = data['SubtitleIndex']
    PPTindex_ = data['PPTIndex']
    AgendaPPTIndex = data['AgendaPPTIndex']
    response = save_message_sql(Agendaindex_, Subtitleindex_, PPTindex_, AgendaPPTIndex)
    # print("response data:", response)
    return response

@app.route('/Award/show_message', methods=["POST", "GET"])
@cross_origin()
def show_message():
    data = show_message_sql()
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    gc.collect()