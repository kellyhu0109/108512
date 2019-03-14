# line_echobot/echobot/views.py

# WebhookHandler version


from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
# from linebot.models import MessageEvent, TextSendMessage, TextMessage
from linebot.models import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    msg = event.message.text
    msg = msg.encode('utf-8')
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

    if event.message.text == "文字":
        print("收到了")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
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


@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Message')
    )


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
