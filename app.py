import requests

from flask import Flask, request, abort, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# เพื่อที่จะ push ขึ้น heroku ได้
from slack.models import Memegen, Slack, parse_text_into_params, image_exists

try:
    from urllib import unquote_plus, quote
except ImportError:
    from urllib.parse import unquote_plus, quote

# --------------------------------------------------------------------------------

app = Flask(__name__)

line_bot_api = LineBotApi('kmQKjpnw+Elj155frdQfSx8RPe0Q0W9raqF3E8C2+XOA7X8Tnho98I0jLQm0GqvPX1gcvJYALhuWrNra+oJEZdemnVhEnTP8JfZg3ferY0g8gwYwNRMqelZw9tm723QrXBlaHxRQ7WrMkAupdnGwkwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c168b6d0f6e838039316872e1163c203')


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

@app.route("/callback", methods=['POST'])
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

# webhook
@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        return 'OK'

# Message ที่ตอบกลับในห้องแชท
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()