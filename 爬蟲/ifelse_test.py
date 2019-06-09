import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.mohw.gov.tw/mp-1.html") #將網頁資料GET下來
soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
sel = soup.select("div.tabContent a") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel

for s in sel:
     print('{}  {}'.format(s['title'], s['href']))       
     titles = soup.select("h2 a")
     t in titles
     if (t['title'] == '焦點新聞' ) :
          # print("1")
          print('{}  {}'.format(s['title'], s['href']))
     elif (t['title'] == '真相說明' ):
          print('{}  {}'.format(s['title'], s['href']))
     elif (t['title'] == '公告訊息' ):
          print('{}  {}'.format(s['title'], s['href']))
     else :
          print("想知道更多請上官網~")
          # print('{}'.format(t['title']))   