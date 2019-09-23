# line_echobot/echobot/views.py

# WebhookHandler version
import datetime
import os
import random
import apiai
import requests

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import UserMessage, News
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import pymysql
from .check import dbcnt

from django_q.tasks import schedule

from bs4 import BeautifulSoup
# from urllib.request import urlretrieve

from django.db import connection

# !/usr/bin/env python

# import urllib
import json
# import os

from flask import Flask
# from flask import request
# from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

DIALOGFLOW_CLIENT_ACCESS_TOKEN = os.environ.get('57d08faed41c4ccf9b949d0b962ce565')
ai = apiai.ApiAI(DIALOGFLOW_CLIENT_ACCESS_TOKEN)


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


# test----------------------------------------------
def r(request):
    return render(request, 'base.html')


# homepage----------------------------------------------
def index(request):
    return render(request, 'index.html')


def tablemenu(request):
    return render(request, 'table/index.html')


def doctor(request):
    return render(request, 'doctor.html')


def medicine(request):
    return render(request, 'medicine.html')


def choose(request):
    return render(request, 'index.html')


# def student(request):
#     students = Student.objects.all()
#     return render(request, 'table/student.html', {
#         'student': students,
#     })
#
#
# def studentdetail(request, pk):
#     detail = get_object_or_404(Student, stuno=pk)
#     # detail = Student.objects.all()
#     return render(request, 'table/studentdetail.html', {
#         'detail': detail,
#     })
#
#
# def studentdetailno(request, pk):
#     detail = get_object_or_404(Student, pk=pk)
#     return render(request, 'table/studentdetail.html', {
#         'detail': detail,
#     })
#
#
# def movie():
#     r = requests.get("https://www.ptt.cc/bbs/MobileComm/index.html")  # 將網頁資料GET下來
#     soup = BeautifulSoup(r.text, "html.parser")  # 將網頁資料以html.parser
#     sel = soup.select("div.title a")  # 取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
#     for s in sel:
#         print(s["href"], s.text)
#
#     target_url = 'https://movies.yahoo.com.tw/'
#     rs = requests.session()
#     res = rs.get(target_url, verify=False)
#     res.encoding = 'utf-8'
#     soup = BeautifulSoup(res.text, 'html.parser')
#     content = ""
#     for index, data in enumerate(soup.select('div.movielist_info h1 a')):
#         if index == 20:
#             return content
#         title = data.text
#         link = data['href']
#         content += '{}\n{}\n'.format(title, link)
#     return content

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# 衛服部
def news():
    target_url = 'https://www.mohw.gov.tw/mp-1.html'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('div.tabContent a')):
        if index == 6:
            return content
        print("data：")
        print(index)
        print(data)
        title = data['title']
        link = data['href']
        # News.objects.create(
        #     title=title, url=link
        # )
        content += '{}\n{}\n\n'.format(title, link)
    return content


@handler.default()
def default(event):
    print(event)
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    # print(index_id)
    sticker_message = StickerSendMessage(
        package_id='11537',  # 1
        sticker_id='52002735'  # sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message
    )


def get_answer(message_text):
    # url = "https://westus.api.cognitive.microsoft.com/qnamaker/v2.0/knowledgebases/{你的QnA Service UUID}/generateAnswer"
    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
        # url,
        json.dumps({'question': message_text}),
        headers={
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '你的Key'
        }
    )
    data = response.json()
    try:
        # 我們使用免費service可能會超過限制（一秒可以發的request數）
        if "error" in data:
            return data["error"]["message"]
        # 這裡我們預設取第一個答案
        answer = data['answers'][0]['answer']
        return answer
    except Exception:
        return "Error occurs when finding answer"


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        # 可以正常 ping 出
        # ------------------------------------
        # print(body)
        # decoded = json.loads(body)
        # user_id = decoded['events'][0]['source']['userId']
        # print(user_id)

        try:
            events = handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        # for event in events:
        #     if isinstance(event, MessageEvent):
        #         answer = get_answer(event.message.text)
        #         line_bot_api.reply_message(
        #             event.reply_token,
        #             TextSendMessage(text=answer)
        #         )
        # print(events)

        # method_1
        # -------------------------
        # resp = {'errorcode': 100, 'detail': 'Get success'}
        # return HttpResponse(json.dumps(resp), content_type="application/json")
        # method_2
        # -------------------------
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# # ================= 客製區 Start =================
# def is_alphabet(uchar):
#     if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
#         print('English')
#         return "en"
#     elif '\u4e00' <= uchar<='\u9fff':
#         print('Chinese')
#         return "zh-tw"
#     else:
#         return "en"
# # ================= 客製區 End =================


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    msg = event.message.text
    msg = msg.encode('utf-8')
    # get user id when reply
    user_id = event.source.user_id
    # print("user_id =", user_id)

    # get user text message
    txt = event.message.text
    # print(txt)

    ai_request = ai.text_request()
    ai_request.session_id = user_id
    ai_request.query = msg

    # 2. 獲得使用者的意圖
    # ai_response = json.loads(ai_request.getresponse().read())
    # user_intent = ai_response['result']['metadata']['intentName']

    # if user_intent == '圖片':
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         ImageSendMessage(
    #           original_content_url='https://i.imgur.com/hCVf4lx.jpg',
    #           preview_image_url='https://i.imgur.com/hCVf4lx.jpg')
    #     )
    # else:
    #     msg = "Sorry，I don't understand"
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=msg)
    #     )

    # connect mysql

    # print('your db len is ' + dbcnt())

    a = list(dbcnt())

    # for x, y in enumerate(a, 0):
    #     print(x, a[y][2])

    if event.message.text == "文字":
        print("收到了")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    # elif event.message.text == "新聞":
    #     a = news()
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == '新聞':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://attach.setn.com/newsimages/2017/02/10/805406-XXL.jpg',
                title='請選擇想要查看的項目~',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='新聞',
                        text='新聞'
                    ),
                    MessageTemplateAction(
                        label='康健雜誌',
                        text='康健雜誌'
                    ),
                    URITemplateAction(
                        label='看更多~~',
                        uri='https://www.commonhealth.com.tw/'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == '康健雜誌':
        mesg = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://as.chdev.tw/web/article/4/f/4/4e6208d3-f726-4b00-9ed8-b7a40ae8d777/A0968004.jpg',
                        action=URIAction(
                            label='40萬人健檢才知高血壓',
                            uri='https://www.commonhealth.com.tw/article/article.action?nid=80116',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://as.chdev.tw/web/article/3/5/4/38564707-5b5e-4d20-9c6c-1aa1a54a69b51567406227.jpg',
                        action=URIAction(
                            label='改善腸躁症',
                            uri='https://www.commonhealth.com.tw/article/article.action?nid=80073',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, mesg)
    elif event.message.text == "貼圖":
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(package_id=1, sticker_id=2)
        )
    elif event.message.text == "圖片":
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url='https://i.imgur.com/UtnXde0.jpg', preview_image_url='https://i.imgur.com/UtnXde0.jpg')
        )
    elif event.message.text == "影片":
        line_bot_api.reply_message(
            event.reply_token,
            VideoSendMessage(original_content_url="https://i.imgur.com/icR54sf.mp4", preview_image_url='https://i.imgur.com/UtnXde0.jpg')
        )
    elif event.message.text == "沒錯":
        print('success')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="恭喜你設定成功!!!")
        )
    elif event.message.text == '預約':
        date_picker = TemplateSendMessage(
            alt_text='請輸入預約提醒日期及時間',
            template=ButtonsTemplate(
                text='請輸入預約提醒日期及時間',
                title='輸入年/月/日 幾時幾分',
                actions=[
                    DatetimePickerAction(
                        label='設定',
                        data='action=buy&itemid=1',
                        mode='datetime',
                        initial='{}T12:00'.format(datetime.date.today()),
                        min='{}T00:00'.format(datetime.date.today()),
                        max='2099-12-31T23:59'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            date_picker
        )
    elif event.message.text == ("設定時間" or "更改"):
        date_picker = TemplateSendMessage(
            alt_text='請輸入時間',
            template=ButtonsTemplate(
                text='請輸入時間',
                title='幾點幾分',
                actions=[
                    DatetimePickerAction(
                        label='設定',
                        data='action=buy&itemid=1',
                        mode='time',
                        initial='{}'.format(str(datetime.datetime.now())[11:16]),
                        min='00:00',
                        max='23:59'
                    )
                ]
            ),
        )
        line_bot_api.reply_message(
            event.reply_token,
            date_picker
        )

        # print(json.dumps(date_picker, separators=[',', ':'], sort_keys=True))

        # json_line = json.dumps(date_picker)
        # decoded = json.loads(json_line)
        # user_time = decoded['postback'][0]['params']['time']
        # print(user_time)

        # print(user_id)

        # print(type(TemplateSendMessage))
    elif event.message.text == "設定日期":
        date_picker = TemplateSendMessage(
            alt_text='請輸入日期',
            template=ButtonsTemplate(
                text='請輸入日期',
                title='輸入年/月/日',
                actions=[
                    DatetimePickerAction(
                        label='設定',
                        data='action=buy&itemid=1',
                        mode='date',
                        initial='2019-05-09',
                        min='2019-05-09',
                        max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            date_picker
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="不好意思我不太知道你的意思")
        )


@handler.add(PostbackEvent)
def handle_post_message(event):
    print("event =", event)

    user_id = event.source.user_id
    print(user_id)
    # line_bot_api.reply_message(
    #         event.reply_token, [
    #             TextMessage(text='您設定的時間是 {}'.format(str(event.postback.params.get('time'))),),
    #             StickerSendMessage(package_id=1, sticker_id=2)
    #         ]
    # )

    time_type = event.postback.params
    day = datetime.date.today()

    # print('time' in time_type)

    count = len(UserMessage.objects.all())+1
    print(count)

    if 'time' in time_type:
        print('您設定的時間是 {} {}:00'.format(datetime.date.today(), str(event.postback.params.get('time'))))

        UserMessage.objects.create(
            no=count, userid=user_id, time='{} {}:00'.format(day, str(event.postback.params.get('time')))
        )

        confirm_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ConfirmTemplate(
                title='再次確認時間',
                text='您設定的時間是 {} 嗎?'.format(str(event.postback.params.get('time'))),
                actions=[
                    MessageTemplateAction(
                        label='沒錯',
                        text='沒錯',
                    ),
                    MessageTemplateAction(
                        label='更改',
                        text='更改',
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            confirm_template
        )
    else:
        print('您設定的時間是 {}'.format(str(event.postback.params.get('datetime'))))

        day = str(event.postback.params.get('datetime'))[:10]
        time = str(event.postback.params.get('datetime'))[11:]

        print(day + ' ' + time)

        UserMessage.objects.create(
            no=count, userid=user_id, time='{} {}:00'.format(day, time)
        )

        confirm_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ConfirmTemplate(
                title='再次確認時間',
                text='您設定的時間是 {} 嗎?'.format(str(event.postback.params.get('datetime'))),
                actions=[
                    MessageTemplateAction(
                        label='沒錯',
                        text='沒錯',
                    ),
                    MessageTemplateAction(
                        label='更改',
                        text='更改',
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            confirm_template
        )
