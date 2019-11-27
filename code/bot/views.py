# line_echobot/echobot/views.py

# WebhookHandler version
import datetime
import os
import random
import requests

from django_q.tasks import schedule
from django_q.models import Schedule
import arrow

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import pymysql

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


def set_time(request):
    return render(request, 'set_time.html')


def choose(request):
    return render(request, 'index.html')


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

    if event.message.text == "文字":
        print("收到了")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
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
    elif event.message.text == "更多新聞":
        a = news()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == '新聞':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://attach.setn.com/newsimages/2017/02/10/805406-XXL.jpg',
                title='請選擇想要查看的項目~',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='更多新聞',
                        text='更多新聞'
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
        print(event.source.user_id)
        print('success')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="恭喜你設定成功!!!")
        )
    elif event.message.text == "查詢藥品":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入藥品名稱~"+"\n\n"+"thanks")
        )
    elif event.message.text == "普拿疼":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="適應症為「退燒、止痛(緩解頭痛、牙痛、咽喉痛、關節痛、神經痛、肌肉酸痛、月經痛 )。」")
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
    elif event.message.text == "輸入看診資訊":
        print("Confirm template")
        Confirm_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ConfirmTemplate(
                title='OCR',
                text='請輸入藥單OCR資訊',
                actions=[
                    PostbackTemplateAction(
                        type='postback',
                        label='Y',
                        text='確認',
                        data='DecideConfirm'
                    ),
                    MessageTemplateAction(
                        label='N',
                        text='取消'
                    )
                ]
            )


        )
        line_bot_api.reply_message(event.reply_token, Confirm_template)

    # content = "{}: {}".format(event.source.user_id, event.message.text)
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=content))

    elif event.message.text == '確認':
        content = "{}: {}".format(event.source.user_id, event.reply_token)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )

        # line_bot_api.reply_message(
        # event.reply_token,
        # TextSendMessage(text="收到")
        # )
    elif event.message.text == '取消':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好吧!掰掰")
        )
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
    elif event.message.text == "RED使用手冊":
        print('success')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="想設定吃藥時間嗎？可以點擊清單圖示或直接輸入「設定時間」即可唷！\n還是想看新聞呢？一樣可以點擊圖示清單來看新聞或是輸入「新聞」來選擇想查看的新聞種類唷~")
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

    if 'time' in time_type:
        print('您設定的時間是 {} {}:00'.format(datetime.date.today(), str(event.postback.params.get('time'))))

        # print('-'*10)
        # current_h = int(datetime.datetime.now().strftime("%H:%M")[:2])
        set_h = int(event.postback.params.get('time')[:2])
        # current_m = int(datetime.datetime.now().strftime("%H:%M")[3:])
        set_m = int(event.postback.params.get('time')[3:])

        # h = int(set_h-current_h)
        # m = int(set_m-current_m)

        # print("h: " + str(set_h-current_h))
        # print("m: " + str(set_m-current_m))
        # print('-'*10)

        user_id = event.source.user_id

        Schedule.objects.create(
            func='bot.tasks.check_time',
            kwargs={'user_id':user_id},
            name='send_message',
            schedule_type=Schedule.MINUTES,
            repeats=1,
            next_run=datetime.datetime.now().replace(hour=set_h, minute=set_m)
            #next_run=arrow.utcnow().replace(hour=9, minute=47)
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
