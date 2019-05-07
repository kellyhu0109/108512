# line_echobot/echobot/views.py

# WebhookHandler version
import datetime
import random

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Student
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
# from linebot.models import MessageEvent, TextSendMessage, TextMessage
from linebot.models import *

import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

# # !/usr/bin/env python
#
# import urllib
# import json
# import os

# from flask import Flask
# from flask import request
# from flask import make_response
#
# # Flask app should start in global layout
# app = Flask(__name__)
#
#
# @app.route("/", methods=['GET'])
# def hello():
#     return "Hello World!"


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


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


def student(request):
    students = Student.objects.all()
    return render(request, 'table/student.html', {
        'student': students,
    })


def studentdetail(request, pk):
    detail = get_object_or_404(Student, stuno=pk)
    # detail = Student.objects.all()
    return render(request, 'table/studentdetail.html', {
        'detail': detail,
    })


# def studentdetailno(request, pk):
#     detail = get_object_or_404(Student, pk=pk)
#     return render(request, 'table/studentdetail.html', {
#         'detail': detail,
#     })


def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('div.movielist_info h1 a')):
        if index == 20:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    msg = event.message.text
    msg = msg.encode('utf-8')

    # get user id when reply
    user_id = event.source.user_id
    print("user_id =", user_id)

    if event.message.text == "文字":
        print("收到了")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    elif event.message.text == "幹":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='十元買早餐 八元買豆干')
        )
    elif event.message.text == "貼圖":
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(package_id=1, sticker_id=2)
        )
    elif event.message.text == "圖片":
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url='https://i.imgur.com/hCVf4lx.jpg', preview_image_url='https://i.imgur.com/hCVf4lx.jpg')
        )
    elif event.message.text == "影片":
        line_bot_api.reply_message(
            event.reply_token,
            VideoSendMessage(original_content_url="https://i.imgur.com/icR54sf.mp4", preview_image_url='https://i.imgur.com/hCVf4lx.jpg')
        )
    elif event.message.text == "最新電影":
        a = movie()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=a)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )


@handler.default()
def default(event):
    print(event)
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
