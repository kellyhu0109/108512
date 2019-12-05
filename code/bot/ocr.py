import jieba
from linebot import LineBotApi, WebhookHandler
from linebot.models import *

LINE_CHANNEL_ACCESS_TOKEN = "m2Q7OLhF/Wk1+QL2YnKnnzGS9X+A5vKLonIYE4fieNlsrp1KxoQIscAxp90UwJONCVmWayFjUwMGjts9jDgkmW/Jcblgu6FPjBtzBpILYcoxWzezrBksvQ239bEyYbh0WOsK6YILTLlN/Ss4ETJ2HwdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


def get_ocr(event):
    with open('../templates/ocr/symbol.txt', "r", encoding='utf8') as f:
        content = f.readlines()

    with open('medicine.txt', "r", encoding='utf8') as m:
        medicine = m.readlines()

    with open('ocr/message.txt', "r", encoding='utf8') as s:
        msg = s.readlines()

    jieba.load_userdict('medicine.txt')

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
            print(i)

    print('='*20)
    print(med_msg)
    print('='*20)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("姓名:" + ocr_name + "\n看診日期:" + ocr_date + "\n院所名稱:" + ocr_h_name + "\n藥品名稱:\n" + med_msg)
    )

    # print("Default Mode: " + "/ ".join(seg_list))
    # print('=' * 20)
