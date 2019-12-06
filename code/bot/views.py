# line_echobot/echobot/views.py

# WebhookHandler version
import datetime
import os
import random
import requests

from django_q.tasks import schedule
from django_q.models import Schedule
import arrow

import emoji
import jieba

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import pymysql

from bs4 import BeautifulSoup
from .models import OcrTable
# from .ocr import get_ocr
# from urllib.request import urlretrieve

from django.db import connection
# from .forms import OcrModelForm

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

prev = {}


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
    ocr_detail = OcrTable.objects.all()
    return render(request, 'set_time.html', {
        'ocr_detail': ocr_detail,
    })


# def set_time(request):
#     form = OcrModelForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('bot:choose')
#
#     return render(request, 'set_time.html', {
#         'form': form,
#     })


def choose(request):
    return render(request, 'index.html')


def get_ocr(event):
    with open('/home/bbkook/108512/code/templates/ocr/symbol.txt', "r", encoding='utf8') as f:
        content = f.readlines()

    with open('/home/bbkook/108512/code/templates/ocr/medicine.txt', "r", encoding='utf8') as m:
        medicine = m.readlines()

    with open('/home/bbkook/108512/code/templates/ocr/message.txt', "r", encoding='utf8') as s:
        msg = s.readlines()

    jieba.load_userdict('/home/bbkook/108512/code/templates/ocr/medicine.txt')

    content = [x.strip() for x in content]
    medicine = [x.strip() for x in medicine]

    msg = event.message.text

    msg = [x.strip() for x in msg]
    msg = ''.join(msg)

    msg = msg.replace(' ', "")
    for i in content:
        msg = msg.replace(i, "")

    # print(msg)
    # print('=' * 20)

    s = msg.find('姓名') + 2
    ocr_name = msg[s:s + 3]
    print("姓名:" + ocr_name)

    s = msg.find('日期') + 2
    ocr_date = msg[s:s + 7]
    print("看診日期:" + ocr_date)

    s = msg.find('院所名稱') + 4
    ocr_h_name = msg[s:s + 7]
    print("院所名稱:" + ocr_h_name)

    # s = msg.find('Lidacin')
    # print("藥品名稱:" + msg[s:s + 30])
    # s = msg.find('Voren')
    # print("藥品名稱:" + msg[s:s + 32])
    # s = msg.find('Strocaine')
    # print("藥品名稱:" + msg[s:s + 34])
    # s = msg.find('Thiamin')
    # print("藥品名稱:" + msg[s:s + 24])
    # s = msg.find('Mucosolvon')
    # print("藥品名稱:" + msg[s:s + 22])
    # print('=' * 20)

    # 精确模式
    seg_list = jieba.cut(msg, cut_all=False)

    med_msg = ""

    for i in seg_list:
        if i in medicine:
            med_msg += i + "\n"
            # print(i)

    print('='*20)
    print(med_msg)
    print('='*20)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="姓名: " + ocr_name + "\n看診日期:" + ocr_date + "\n院所名稱:" + ocr_h_name + "\n藥品名稱:\n" + med_msg
        )
    )

    # print("Default Mode: " + "/ ".join(seg_list))
    # print('=' * 20)


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

    # ---------------------------------------------------
    msg_ids = ['這樣不行喔', '安內母湯喔', '色即是空 空即是色', '我什麼也沒看到', '（以上我省略', 'ㄎㄎ', 'ㄏㄏ']
    index_id = random.randint(0, len(msg_ids) - 1)
    b_msg = msg_ids[index_id]

    x_words_ids = ['在非洲，每六十秒，就有一分鐘過去', '凡是每天喝水的人，有高機率在100年內死去', '每呼吸60秒，就減少一分鐘的壽命',
                   '你只要蹲得越低越久腳就越酸', '美國人三歲就會說講英文', '成功的男人背後 都有一個脊椎', '很好笑 哈哈', '人家有的是背景，咱有的是背影',
                   '鹹魚翻身，還是鹹魚', '託夢才是人類歷史上最早的無線通訊方式', '我像草一樣，不能自拔', '樹不要皮，必死無疑；人不要臉，天下無敵']
    x_index_id = random.randint(0, len(x_words_ids) - 1)
    x_words_msg = x_words_ids[x_index_id]

    joke = ['有一天在路上一個人的書掉了\n\n 我他說:「哈囉~你書掉囉」\n\n他回我：「我慧瑩」']

    bad_words = ['幹', '北七', '白癡', '靠', '靠邀', '靠腰', '靠北', '幹你娘', '幹你老師', '西八']
    all_hello = ['你好', 'hello', 'hi', '嗨', '哈囉', '안녕', '안녕하세요', 'Hi', 'Hello']
    x_words = ['幹話', '你會講幹話嘛', '講幹話']
    # ---------------------------------------------------

    # ---------------------------------------------------
    medicine_dict = {
        '普拿疼': '退燒、止痛(緩解頭痛、牙痛、咽喉痛、關節痛、神經痛、肌肉酸痛、月經痛 )',
        '咳止糖漿': '緩解感冒之各種症狀（流鼻水，鼻塞，打噴嚏，喀痰）',
        '循利寧': '末梢血行障礙之輔助治療',
        '斯斯感冒膠囊': '緩解感冒之各種症狀（咽喉痛、發燒、頭痛、關節痛、肌肉痛、流鼻水、鼻塞、打噴嚏、咳嗽）',
        '斯斯': '緩解感冒之各種症狀（咽喉痛、發燒、頭痛、關節痛、肌肉痛、流鼻水、鼻塞、打噴嚏、咳嗽）',
        '阿斯匹靈': '退燒、止痛（緩解頭痛、牙痛、咽喉痛、關節痛、神經痛、肌肉酸痛、月經痛）',
        '胃腸藥': '消化制酸、健胃、整腸',
        '胃散': '胃酸過多、消化不良、腸內異常醱酵、腹部膨脹',
        '整腸丸': '腸內異常醱酵、消化不良、腸炎',
        '若元錠': '消化不良、食慾不振、胃腸內異常發酵、便秘',
        'wakamoto': '消化不良、食慾不振、胃腸內異常發酵、便秘',
        '維骨力': '緩解退化性關節炎之疼痛',
        'Shin Lulu': '緩解感冒之各種症狀(咽喉痛、畏寒、發燒、頭痛、關節痛、肌肉酸痛、流鼻水、鼻塞、打噴嚏、咳嗽、喀痰)',
        '欣樂樂': '緩解感冒之各種症狀(咽喉痛、畏寒、發燒、頭痛、關節痛、肌肉酸痛、流鼻水、鼻塞、打噴嚏、咳嗽、喀痰)',
        '新樂樂': '緩解感冒之各種症狀(咽喉痛、畏寒、發燒、頭痛、關節痛、肌肉酸痛、流鼻水、鼻塞、打噴嚏、咳嗽、喀痰)',
        '新ルル': '緩解感冒之各種症狀(咽喉痛、畏寒、發燒、頭痛、關節痛、肌肉酸痛、流鼻水、鼻塞、打噴嚏、咳嗽、喀痰)',
    }
    # ---------------------------------------------------

    if event.message.text == "文字":
        print("收到了")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    elif event.message.text == "現在時間":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(datetime.datetime.now())[11:16])
        )
    elif event.message.text == "設定時間":
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
    elif event.message.text == "更改":
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
                thumbnail_image_url='https://www.garygoh.com.au/images/news/News%20image.jpg',
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
        # print(event.source.user_id)
        # print('success')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="恭喜你設定成功!!!")
        )
    elif event.message.text == "查詢藥品":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入藥品名稱~")
        )
    # elif event.message.text == "OCR":
    #     prev[event.source.user_id] = 'OCR'
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text="請輸入藥單資訊")
    #     )
    # elif event.message.text == "普拿疼":
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text="適應症為「退燒、止痛(緩解頭痛、牙痛、咽喉痛、關節痛、神經痛、肌肉酸痛、月經痛 )。」")
    #     )
    elif event.message.text in medicine_dict:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="適應症：\n" + medicine_dict[event.message.text])
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
        line_bot_api.reply_message(
            event.reply_token,
            Confirm_template
        )
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
        e = chr(0x100080)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="RED使用手冊：\n\n✔設定提醒時間\n    ▶準時吃藥、回診不錯過\n\n✔藥物使用須知\n   ▶輸入藥名/OCR照相輸入藥名，深入瞭解藥物資訊\n\n✔最新新聞\n▶獲取藥物界、疾病界資訊，最新新聞不錯過\n\n✔群組功能\n   ▶將本帳號加入家人或朋友群組，互相提醒，增進彼此感情\n\n\n🔺可使用選單輸入或打字自行輸入，啟動以上功能")
        )
    elif event.message.text == "廢物":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="回收")
        )
    elif event.message.text == "87":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="56")
        )
    elif event.message.text == "八七":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="五十六")
        )
    elif event.message.text == "你真的是機器人嗎":
        e = chr(0x100096)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我不是\n我是你的心上人" + e)
        )
    elif event.message.text == "你是男的還是女的":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我是個跨性別者")
        )
    elif event.message.text in bad_words:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=b_msg)
        )
    elif event.message.text in all_hello:
        e = chr(0x100001)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你好~我是你的小幫手 RED" + e)
        )
    elif event.message.text == "RED":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="嗨~有什麼需要幫忙的嘛")
        )
    elif event.message.text in x_words:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=x_words_msg)
        )
    elif event.message.text == "笑話":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=joke[0])
        )
    elif event.message.text == "OCR":
        prev[event.source.user_id] = "OCR"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的~請輸入您的藥單資訊~")
        )
    else:
        if event.source.user_id not in prev:
            e = chr(0x100010)
            e2 = chr(0x10008D)
            prev.update({event.source.user_id: ''})
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='不好意思 我不太清楚你的意思 ' + e + "麻煩你再說一次，或是可以點擊下方選單「RED 使用手冊」了解更多" + e2),
                    StickerSendMessage(package_id=11539, sticker_id=52114129)
                ]
            )
        elif prev[event.source.user_id] == 'OCR':
            get_ocr(event)
            prev.update({event.source.user_id: ''})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='好的~請輸入您的OCR掃描~')
            )
        else:
            e = chr(0x100010)
            e2 = chr(0x10008D)
            prev.update({event.source.user_id: ''})
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='不好意思 我不太清楚你的意思 ' + e + "麻煩你再說一次，或是可以點擊下方選單「RED 使用手冊」了解更多" + e2),
                    StickerSendMessage(package_id=11539, sticker_id=52114129)
                ]
            )

    print(prev)

    # if prev[event.source.user_id] == 'OCR':
    #     get_ocr()
    # else:
    #     print('nothing')


@handler.add(PostbackEvent)
def handle_post_message(event):
    print("event =", event)

    # user_id = event.source.user_id
    # group_id = event.source.group_id
    #
    # print(user_id)
    # print(group_id)

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
        # print('您設定的時間是 {} {}:00'.format(datetime.date.today(), str(event.postback.params.get('time'))))

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

        if event.source.type == 'group':
            group_id = event.source.group_id
        else:
            group_id = ""

        user_id = event.source.user_id
        # group_id = event.source.group_id

        Schedule.objects.create(
            func='bot.tasks.check_time',
            kwargs={'user_id': user_id, 'group_id': group_id},
            name='send_message',
            schedule_type=Schedule.MINUTES,
            repeats=1,
            next_run=datetime.datetime.now().replace(hour=set_h, minute=set_m)
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
