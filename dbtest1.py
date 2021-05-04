# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 15:38:09 2021

@author: cloud
"""

from flask import Flask
from flask import request,abort,render_template
from flask_sqlalchemy import SQLAlchemy
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi,WebhookHandler
from linebot.models import MessageEvent,TextMessage,TextSendMessage

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://jtddnlrlwslvde:a8d69b75095bead5c914349b64baad621c29224cf956e5a51f06996a4fb8e58c@ec2-3-212-75-25.compute-1.amazonaws.com:5432/dojvf1o5jetp7'
db=SQLAlchemy(app)

line_bot_api=LineBotApi('yxtGR78w8l+EZb8GT4Vn1jfVWsV1kS856OtUfSbT+TUTtplgpb2ISmhXabv+6l3A74Q60c+XTEoyXQ6LvGUy813C/TY72WeL920T8qIJbG97CKQX4tEyicuwCq0fKA/KB88qcwXk6GvQhTUlidSbNwdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('c05f2a87ac67ce93bd8fc407dbeb43a1')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@flex':
        sendFlex(event)
def sendFlex(event):
    sql_cmd="insert into students values(sname='Asf',sgrade=11,smajor='AAA',sdate=current_date,stime=localtime(0));"
    db.engine.execute(sql_cmd)
    
    
if __name__=='__main__':
    app.run()
    