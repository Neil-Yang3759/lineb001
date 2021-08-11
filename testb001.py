# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:43:39 2021

@author: cloud
"""
from flask import request,abort,render_template,Flask
from flask_sqlalchemy import SQLAlchemy
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi,WebhookHandler
from linebot.models import PostbackEvent,MessageEvent,TextMessage,TextSendMessage,BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage, URIAction

#import bluetooth

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xwvwqwtfmgxaxm:ed1e4d1cca4493d17f313adeb3013395e2e35d7daf4a9ca264dfcf1ea7da4272@ec2-174-129-225-160.compute-1.amazonaws.com:5432/dfhrokp4l321dc'
db=SQLAlchemy(app)

line_bot_api=LineBotApi('yxtGR78w8l+EZb8GT4Vn1jfVWsV1kS856OtUfSbT+TUTtplgpb2ISmhXabv+6l3A74Q60c+XTEoyXQ6LvGUy813C/TY72WeL920T8qIJbG97CKQX4tEyicuwCq0fKA/KB88qcwXk6GvQhTUlidSbNwdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('c05f2a87ac67ce93bd8fc407dbeb43a1')
liffid1 = '1655833971-8JP5EZR1'
liffid2 = '1655833971-eVBEndlD'


        
@app.route('/page1')
def page1():
	return render_template('member.html', liffid = liffid1)
@app.route('/page2')
def page2():
	return render_template('reschedule.html', liffid = liffid2)

@app.route('/callback',methods=['POST'])
def callback():
    signature=request.headers['X-Line_Signature']
    body=request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '動作 1':
        sendFlex(event)
    elif mtext[:3] == '###' and len(mtext) > 3:
        member(event, mtext)
    elif mtext[:4] == '####' and len(mtext) > 4:
        reschedule(event, mtext)
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

# @handler.add(PostbackEvent)
# def handle_postback(event):
#     # postback 資料
#     data = event.postback.data
#     # 使用者Id
#     userId = event.source.user_id
    
#     # 下一頁
#     if data == "action=next":
#         # 設定個別用戶選單
#         line_bot_api.link_rich_menu_to_user(userId, 'richmenu-f3278452270e0ca1c986d2dcdb33aba4')
#     elif data == "action=next2":
#         line_bot_api.link_rich_menu_to_user(userId, 'richmenu-b587ba7dcda53980766b97e2bfaadd11')
#     # 上一頁
#     elif data == "action=prev":
#         line_bot_api.unlink_rich_menu_from_user(userId)
#     # elif data == "action=prev":
#     #     # 移除個別用戶選單
#     #     line_bot_api.link_rich_menu_from_user(userId,'richmenu-688c0086e723359b2c81d48441b96eb4')
#     elif data == "action=prev2":
#         line_bot_api.link_rich_menu_from_user(userId,'richmenu-10f7a761acff4f3de43996a9d3946f31')

def sendFlex(event):

    userId = event.source.user_id
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=userId+': '+event.message.text))

def member(event, mtext):
    try:
        flist = mtext[3:].split('/')
        # insert into students(sid,sname,sgrade,smajor,sdate,stime) values('B10702004','yang',3,'CS',current_date,localtime(0));
        if flist[0] == 'i':
            sql_cmd="insert into student values ('"+flist[1]+"','"+flist[2]+"',"+flist[3]+",'"+flist[4]+"');"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='insert complete!'))
        # elif flist[0] == 'u':
        #     sql_cmd="update students set sname='"+flist[2]+"',sgrade="+flist[3]+",smajor='"+flist[4]+"',sdate=current_date,stime=localtime(0) where sid = ('"+flist[1]+"');"
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='update complete！'))
        elif flist[0] == 'd':
            sql_cmd="delete from student where sid =  '"+flist[1]+"';"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='delete complete！'))
        # elif flist[0] == 'q':
        #     sql_cmd="select * from students where sid = '"+flist[1]+"';"
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='search complete！'))
            
        db.engine.execute(sql_cmd)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def reschedule(event, mtext):
    try:
        flist = mtext[3:].split('/')
        # insert into students(sid,sname,sgrade,smajor,sdate,stime) values('B10702004','yang',3,'CS',current_date,localtime(0));
        if flist[0] == 'i':
            sql_cmd="insert into students (sid,sname,sgrade,smajor,sdate,stime) values ('"+flist[1]+"','"+flist[2]+"',"+flist[3]+",'"+flist[4]+"',current_date,localtime(0));"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='insert complete!'))
        elif flist[0] == 'u':
            sql_cmd="update students set sname='"+flist[2]+"',sgrade="+flist[3]+",smajor='"+flist[4]+"',sdate=current_date,stime=localtime(0) where sid = ('"+flist[1]+"');"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='update complete！'))
        elif flist[0] == 'd':
            sql_cmd="delete from students where sid =  '"+flist[1]+"';"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='delete complete！'))
        elif flist[0] == 'q':
            sql_cmd="select * from students where sid = '"+flist[1]+"';"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='search complete！'))
            
        db.engine.execute(sql_cmd)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

if __name__=='__main__':
    app.run()
    
