import requests

from flask import Flask, request, abort, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
)


app = Flask(__name__)

channelAccessToken = 'kmQKjpnw+Elj155frdQfSx8RPe0Q0W9raqF3E8C2+XOA7X8Tnho98I0jLQm0GqvPX1gcvJYALhuWrNra+oJEZdemnVhEnTP8JfZg3ferY0g8gwYwNRMqelZw9tm723QrXBlaHxRQ7WrMkAupdnGwkwdB04t89/1O/w1cDnyilFU='
channelSecret = 'c168b6d0f6e838039316872e1163c203'

line_bot_api = LineBotApi(channelAccessToken)
handler = WebhookHandler(channelSecret)


@app.route('/')
def hello():
    return 'Nice to see you!'

@app.route('/ping')
def pong():
    return 'pong!'

@app.route('/covid')
def covid():
    r = requests.get('https://covid19.th-stat.com/api/open/today')
    print(r) # <Response [200]>
    print(r.json())
    data = r.json() # python dictionary
    return jsonify(data)

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# Message ที่ตอบกลับในห้องแชท
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message)

    # ทำให้ที่พิมพ์เข้ามาเป็นตัวพิมเล็ก
    eventText = event.message.text.lower()

    # return 200 OK for line webhook verify
    if(eventText == 'hello, world'):
        return 'OK'

    # trim space หน้า หลัง
    trimmed = eventText.strip()

    if(trimmed == 'cbot'):
        message = "try 'cbot hi' or 'cbot covid'"
        reply_message = TextSendMessage(message)
    else:
        # split string by white space
        splited = trimmed.split(" ")
        print(splited)
        if(splited[0] == 'cbot'):
            if(splited[1] == 'hi'):
                message = "I'm C'Bot. Nice to meet you."
                reply_message = TextSendMessage(message)
            elif(splited[1] == 'covid'):
                r = requests.get('https://covid19.th-stat.com/api/open/today')
                data = r.json() # python dictionary เอาข้อมูลที่อยู่ในแต่ละอัน data['key']
                message = "ยืนยันยอดผู้ป่วย COVID-19 ในไทย \nอัพเดตล่าสุดเมื่อ {} \nยอดผู้ติดเชื้อสะสม {} คน (🔺{}) \nรักษาหาย {} คน (🔺{}) \nกำลังรักษา {} คน (🔺{}) \nเสียชีวิต {} คน (🔺{}) \n \nที่มา : {} ".format(data['UpdateDate'],
                           data['Confirmed'], data['NewConfirmed'], data['Recovered'], data['NewRecovered'], 
                           data['Hospitalized'], data['NewHospitalized'], data['Deaths'], data['NewDeaths'], data['Source'])
                reply_message = TextSendMessage(message)
            elif(splited[1] == 'symptoms'):
                # Send image message
                reply_message = ImageSendMessage(
                    original_content_url='https://www.isranews.org/images/2020/isranews/2/covid0803631.jpg',
                    preview_image_url='https://www.isranews.org/images/2020/isranews/2/covid0803631.jpg'
                )
            elif(splited[1] == 'working'):
                # Send flex message
                reply_message = FlexSendMessage(
                    altText = "This is a flex message",
                    contents = {
                        "type": "bubble",
                        "header": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Where do you work today?",
                                    "weight": "bold",
                                    "size": "lg",
                                    "align": "center"
                                }
                            ]
                        },
                        "hero": {
                            "type": "image",
                            "url": "https://www.romania-insider.com/sites/default/files/styles/article_large_image/public/2020-04/remote_working_laptop_-_photo_pattanaphong_khuankaew_-_dreamstime.com_.jpg",
                            "size": "full",
                            "aspectRatio": "2:1"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                # แนวนอน แถว 1
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "md",
                                    "contents": [
                                        {
                                            "type": "button",
                                            "style": "link",
                                            "action": {
                                                "type":"message",
                                                "label":"Home",
                                                "text":"Home"
                                            }
                                        },
                                        {
                                            "type": "separator"   # เส้นกั้นแนวตั้ง
                                        },
                                        {
                                            "type": "button",
                                            "style": "link",
                                            "action": {
                                                "type":"message",
                                                "label":"Office",
                                                "text":"Office"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "type": "separator"  # เส้นกั้นแนวนอน
                                },
                                # แนวนอน แถว 2
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "md",
                                    "contents": [
                                        {
                                            "type": "button",
                                            "style": "link",
                                            "action": {
                                                "type":"message",
                                                "label":"Client's Office",
                                                "text":"Client's Office"
                                            }
                                        },
                                        {
                                            "type": "separator"   # เส้นกั้นแนวตั้ง
                                        },
                                        {
                                            "type": "button",
                                            "style": "link",
                                            "action": {
                                                "type":"message",
                                                "label":"Absent",
                                                "text":"Absent"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                )
            else:
                message = "Sorry, I can't answer you that."
                reply_message = TextSendMessage(message)


    line_bot_api.reply_message(
        event.reply_token,
        reply_message)


if __name__ == "__main__":
    app.run()