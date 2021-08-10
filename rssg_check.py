import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re
from win10toast import ToastNotifier
import json

session = requests.Session()
url = "https://www.wuxiaworld.co/Reincarnation-Of-The-Strongest-Sword-God/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
default = """Keguan Please wait a moment"""

chapters_url = "https://www.webnovel.com/apiajax/chapter/GetChapterList?_csrfToken=gmHD3tL4Mqye1C9obbvCopkTukVRwcLYifO4omPu&bookId=8527113906000305&_=1584706561069"
while True:
    response = session.get(chapters_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    content = json.loads(soup.text.replace("â", "'"))
    newChapterTime = content['data']['bookInfo']['newChapterTime']
    if 'minutes ago' not in newChapterTime and 'hour ago' not in newChapterTime:
        print(newChapterTime)
        time.sleep(60)
    else:
        newChapterIndex = str(content['data']['bookInfo']['newChapterIndex'])
        break

while True:
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find(attrs={"id": "list"})

    if newChapterIndex not in content.text:
        print(f"Home page still not updated. Time : {datetime.now().time()}")
    else:
        break
    time.sleep(60)

new = soup.find('a', string=re.compile(newChapterIndex))
chapter_url = url + new['href']


while True:
    response = session.get(chapter_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find(attrs={"class": "box_con"})
    if default in content.text:
        print(f"Chapter {newChapterIndex} still not updated. Time : {datetime.now().time()}")
    else:
        print(f"Chapter is out. Time : {datetime.now().time()}")
        toaster = ToastNotifier()
        toaster.show_toast("RSSG!", "NEW CHAPTER OUT!", threaded=True, icon_path=None, duration=30)
        break
    time.sleep(30)

while True:
    toaster.show_toast("RSSG!", "NEW CHAPTER OUT!", threaded=True, icon_path=None, duration=3)
    time.sleep(20)
