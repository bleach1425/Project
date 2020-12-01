import requests
from bs4 import BeautifulSoup

header_data = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6"
}

r = requests.get("https://tw.yahoo.com/")
r.encoding = "utf-8"

bs = BeautifulSoup(r.text, "html.parser")
# print(bs)
title = bs.find_all("ul", {"class" : "Mb(0) Mt(0) Mstart(56.5%) Pstart(14px)"})

# for n in title:
#     print(n.li.a.span.text)
#     print(n.li.a.get("href"))
#     print('-------------------------------------------------------------------------------')


for n in title:
    print(n.li)
