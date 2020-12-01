import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import csv


def login(facebook_path):
    chrome.get(facebook_path)
    chrome.find_element_by_id("email").send_keys("rubio6969s@gmail.com")
    time.sleep(1)
    chrome.find_element_by_id('pass').send_keys("rubio8787s")
    time.sleep(1)
    button = chrome.find_element_by_id('u_0_b')
    time.sleep(1)
    button.click()
    time.sleep(5)

    return "登入成功"

def get_code():
    with open("Code.json", mode="r", encoding="utf-8") as f:
        data = f.read()
        json_data = json.loads(data)
        return json_data

chrome =  webdriver.Chrome("./chromedriver.exe")
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}


Code = get_code()
facebook_path="https://www.facebook.com/"
facebook_path1="https://www.facebook.com/profile.php?id="
options.add_experimental_option('prefs', prefs)
options.add_argument("--disable-notifications")

a = True
name_list=[]
id_list=[]
lst_list=[]

about_list=["&sk=about_overview", "&sk=about_work_and_education", "&sk=about_places", "&sk=about_contact_and_basic_info", "&sk=about_family_and_relationships", "&sk=about_details", "&sk=about_life_events"]
for i, n in enumerate(Code["Code"]):
    print("正在處理第", i ,"位使用者", n)
    content_list=[]
    # if i == 0:
    href = facebook_path1 + n
    print("前往的網址", href)
        # id_list.append(n)
    # else:
    #     print("前往的網址", )
    if a == True:
        login(facebook_path)
        a = False
    for about_len, about in enumerate(about_list):
        time.sleep(1)
        about_href = href + about
        chrome.get(about_href)
        time.sleep(3)
        name = chrome.find_elements_by_tag_name("h1")
        for n in name:
            pass
        user_name = n.text
            # if about_len == 0:
        # content = chrome.find_element_by_class_name("c9zspvje")

        content = chrome.find_elements_by_tag_name("span")
        for content_word in content[45:48]:
            content_list.append(content_word.text)
    time.sleep(5)
    with open("User.csv", mode="a", encoding="utf-8") as f:
        writer = csv.writer(f)
        target_data = ",".join(i for i in content_list)
        print("輸入csv的資料:",user_name, target_data)
        writer.writerow([user_name, target_data])
    time.sleep(20)