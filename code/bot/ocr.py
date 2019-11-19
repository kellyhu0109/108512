import jieba

with open('ocr/symbol.txt', "r", encoding='utf8') as f:
    content = f.readlines()

# with open('medicine123.txt', "r", encoding='utf8') as m:
#     medicine = m.readlines()

with open('ocr/message.txt', "r", encoding='utf8') as s:
    msg = s.readlines()

jieba.load_userdict('medicine123.txt')

content = [x.strip() for x in content]
# medicine123 = [x.strip() for x in medicine]
msg = [x.strip() for x in msg]
msg = ''.join(msg)

msg = msg.replace(' ', "")
for i in content:
    msg = msg.replace(i, "")

# print(msg)
# print('=' * 20)

s = msg.find('娃名') + 2
ocr_name = msg[s:s + 3]
print("姓名:" + msg[s:s + 3])

s = msg.find('目期') + 2
ocr_date = msg[s:s + 7]
print("看診日期:" + msg[s:s + 7])

s = msg.find('院所名稱') + 4
ocr_h_name = msg[s:s + 7]
print("院所名稱:" + msg[s:s + 7])

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

print("Default Mode: " + "/ ".join(seg_list))
print('=' * 20)
