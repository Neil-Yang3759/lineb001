from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('yxtGR78w8l+EZb8GT4Vn1jfVWsV1kS856OtUfSbT+TUTtplgpb2ISmhXabv+6l3A74Q60c+XTEoyXQ6LvGUy813C/TY72WeL920T8qIJbG97CKQX4tEyicuwCq0fKA/KB88qcwXk6GvQhTUlidSbNwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c05f2a87ac67ce93bd8fc407dbeb43a1')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])

#發訊給
#to = "U6cc08331f3d9b02959c4a7d167f88b8d" 
#YOUR USER ID

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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text=event.message.text)
    content = "{}: {}".format(event.source.user_id, event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
    #message = TextSendMessage(text="cchaha")
    #line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
#-------------
#from linebot import LineBotApi
#from linebot.models import TextSendMessage
#from linebot.exceptions import LineBotApiError

#line_bot_api = LineBotApi('vyvfuUCeAp07nbIRvR7uaY4weKwV+fJ1bZNt0WtIIktFpZZxSr2DlgrSXckPsBgNz6NRmAuCcE4f8i4dN0w4Sn+vZmtC2szSvJIhi+m9mGq+Y/n7ziQVe5JkPUs0BKXq8Nak02taRQsMtHDYr/a1RgdB04t89/1O/w1cDnyilFU=')

#try:
#    line_bot_api.push_message('U6cc08331f3d9b02959c4a7d167f88b8d', TextSendMessage(text='Hello World!'))
#except LineBotApiError as e:
    # error handle
#    raise e