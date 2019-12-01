from linebot import LineBotApi, WebhookHandler
from linebot.models import *

LINE_CHANNEL_ACCESS_TOKEN = "m2Q7OLhF/Wk1+QL2YnKnnzGS9X+A5vKLonIYE4fieNlsrp1KxoQIscAxp90UwJONCVmWayFjUwMGjts9jDgkmW/Jcblgu6FPjBtzBpILYcoxWzezrBksvQ239bEyYbh0WOsK6YILTLlN/Ss4ETJ2HwdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


def check_time(user_id, group_id):
    # user_id = 'U5ce420cd3d41e910d5ecbeedf928322e'
    line_bot_api.push_message(user_id, TextSendMessage(text='您設定的時間到囉~'))
    if group_id == "":
        print("no group")
    else:
        line_bot_api.push_message(group_id, TextSendMessage(text='您設定的時間到囉~'))


def sayHello():
    print("Hello World!!!!!!!")
