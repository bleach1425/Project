# !/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from django.utils.crypto import get_random_string
import boto3
import time
from random import Random
from hashlib import sha256
from Crypto.Cipher import AES
import base64

vi = '$yN)I!/og[1l6}4q'
key = '5$gFWWR(Ox(i_ACe'

def create_salt(length = 8):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789~!@#$%^&*(_)+=[]{}\|?/'
    len_chars = len(chars) - 1
    random = Random()
    for i in range(length):
        salt += chars[random.randint(0, len_chars)]
    return salt

def AES_Encrypt(key, data):
    pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16)
    data = pad(data)
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    encodestrs = base64.b64encode(encryptedbytes)
    enctext = encodestrs.decode('utf8')
    return enctext
 
def AES_Decrypt(key, data):
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted

def put_data_caoling(data, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Caoling')
    response = table.put_item(Item=data)
    return response

def put_data_shuili(time_, account_, location_, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")    
    table = dynamodb.Table('Shuili')
    response = table.put_item(
        Item={
            "Time": time_,
            'account':account_,
            'location':location_
        }
    )
    return response

def caoling_signup(data, i, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Account')
    if i == 1:
        response = table.put_item(Item = data)
    else:
        if caoling_signin(data['account'], data['password'], 0) == -1:
            data['salt'] = create_salt()
            data['password'] = AES_Encrypt(key, data['password'] + data['salt'])
            response = table.put_item(Item = data)
            return response
        else:
            return -1
        
def shuili_signup(data, i, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Shuili_Account')
    if i == 1:
        response = table.put_item(Item = data)
    else:
        if shuili_signin(data['account'], data['password'], 0) == -1:
            data['salt'] = create_salt()
            data['password'] = AES_Encrypt(key, data['password'] + data['salt'])
            response = table.put_item(Item = data)
            return response
        else:
            return -1
    
def shuili_signin(account, password, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Shuili_Account')
    response = table.get_item(Key={'account' : account})
    try:
        aes_obj = AES_Encrypt(key, password + response['Item']['salt'])
        if  aes_obj == response['Item']['password']:
            return 1
        else:
            return 0
    except KeyError:
        return -1
    
def caoling_signin(account, password, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Account')
    response = table.get_item(Key={'account' : account})
    try:
        aes_obj = AES_Encrypt(key, password + response['Item']['salt'])
        if  aes_obj == response['Item']['password']:
            return 1
        else:
            return 0
    except KeyError:
        return -1
    
def get_shuili_points(account, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Shuili_Account')
    response = table.get_item(Key={'account' : account})
    return response['Item']['shuili_points']

def get_caoling_info(account, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Account')
    response = table.get_item(Key={'account' : account})
    return response['Item']

def update_shuili_points(account, points, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Shuili_Account')
    data = table.get_item(Key={'account' : account})
    data['Item']['shuili_points'] = points
    response = table.put_item(Item=data['Item'])
    return response

def update_caoling_points(account, points, dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = "AKIAVF7XD7CKGIIG666F", aws_secret_access_key = "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", region_name="ap-east-1")
    table = dynamodb.Table('Account')
    data = table.get_item(Key={'account' : account})
    data['Item']['caoling_points'] = str(int(data['Item']['caoling_points']) + int(points))
    if int(data['Item']['caoling_points']) < 0:
        response = 'Error!'
    else:
        table.put_item(Item=data['Item'])
        response = data['Item']['caoling_points']
    return response
app = Flask(__name__)
@app.route('/CaolingDB', methods = ['GET','POST'])
def get_caoling_req():
    data = request.get_json()
    put_data_caoling(data, 0)
    response = 'Success!'
    return response, 200

@app.route('/ShuiliDB', methods = ['GET','POST'])
def get_shuili_req():
    time_ = request.args['Time']
    account_ = request.args['account']
    location_ = request.args['location']
    put_data_shuili(time_, account_, location_, 0)
    response = 'Success!'
    return response, 200

@app.route('/signup1', methods = ['GET', 'POST']) ##Shuili
def signup1_req():
    data = {
        "account": request.args['email'],
        "name": request.args['userName'],
        "password": request.args['password'],
        "birthday": request.args['birthDay'],
        "phone_number": request.args['phone'],
        "blood_type": request.args['blood'],
        "city": request.args['area1'],
        "district": request.args['area2'],
        "constellation": request.args['constellation'],
        "shuili_points": '0',
        }
    if shuili_signup(data, 0) != -1:
        return 'Success!', 200
    else:
        return 'Error', 200

@app.route('/signup', methods = ['GET','POST']) ##Caoling
def signup_req():
    data = request.get_json()
    data['caoling_points'] = '500'
    data['recommand'] = '0'
    usercode = data['usercode']
    del data['usercode']

    if usercode == '':
        data['recommand_by'] = 'yinglijob268@gmail.com'
        response = get_caoling_info('yinglijob268@gmail.com', 0)
        response['recommand'] = str(int(response['recommand'])+1)
        if response['recommand'] == '3':
            response['caoling_points'] = str(int(response['caoling_points'])+500)
            response['recommand'] = '0'
        caoling_signup(response, 1, 0)
        if caoling_signup(data, 0, 0) != -1:
            return 'Success!', 200
        else:
            return 'Failed!', 200

    elif usercode == 'ehonehon':
        data['recommand_by'] = '繪本旅館'
        if caoling_signup(data, 0, 0) != -1:
            return 'Success!', 200
        else:
            return 'Failed!', 200
    else:
        try:
            response = get_caoling_info(usercode, 0)
            response['recommand'] = str(int(response['recommand'])+1)
            if response['recommand'] == '3':
                response['caoling_points'] = str(int(response['caoling_points'])+500)
                response['recommand'] = '0'
            caoling_signup(response, 1, 0)
            data['caoling_points'] = '500'
            data['recommand_by'] = usercode
            if caoling_signup(data, 0, 0) != -1:
                return 'Success!', 200
            else:
                return 'Failed!', 200
        except KeyError:
            return 'Error!', 200

@app.route('/signin', methods = ['GET','POST'])
def signin_req():
    account = request.args['account']
    password = request.args['password']
    place = request.args['place']
    if place == '0':                                    ##Shuili
        response = shuili_signin(account, password, 0)
        if response == 1:
            points = get_shuili_points(account, 0)
            return str(points), 200
        if response == 0:
            return 'Wrong password!', 200
        else:
            return 'No such account!', 200
    else:                                              ##Caoling
        response = caoling_signin(account, password, 0)
        if response == 1:
            return "Success!",200
        if response == 0:
            return 'Error!', 200
        else:
            return 'Empty!', 200


@app.route('/get_shuili_points', methods = ['GET','POST'])
def shuili_points():
    account = request.args['account']
    response = get_shuili_points(account, 0)
    return str(response), 200

@app.route('/get_caoling_info', methods = ['GET','POST'])
def caoling_info():
    account = request.args['account']
    response = get_caoling_info(account, 0)
    return response, 200

@app.route('/update_shuili_points', methods = ['GET','POST'])
def new_shuili_points():
    account = request.args['account']
    points = request.args['points']
    response = update_shuili_points(account, points, 0)
    return response, 200

@app.route('/update_caoling_points', methods = ['GET','POST'])
def new_caoling_points():
    account = request.args['account']
    points = request.args['points']
    response = update_caoling_points(account, points, 0)
    return response, 200



if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000)
