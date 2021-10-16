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

line_bot_api=LineBotApi('mQXBdpy2wiCQVUxQlEQySiv6RAYJdpxgpyDGmus06yL2yj2DTfUGflfjYR4RRobeJ5EFoI7v2aWLDU7OVpU7mgoOywZswmZTiqFOZV4Ttb0Dr6PP1xb4UtHuQqjekMIscE/W9MlR8nwl3IOhJzVBYQdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('d560ad94729a14fb6bda0e47ddf67219')
liffid1 = '1655833971-8JP5EZR1'
liffid2 = '1655833971-eVBEndlD'
liffid3 = '1655833971-10qjl0re'

        
@app.route('/page1')
def page1():
	return render_template('student.html', liffid = liffid1)
@app.route('/page2')
def page2():
	return render_template('reschedule.html', liffid = liffid2)
@app.route('/page3')
def page3():
	return render_template('teacher.html', liffid = liffid3)
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
        student(event, mtext)
    elif mtext[:4] == '####' and len(mtext) > 4:
        reschedule(event, mtext)
    elif mtext[:3] == '##$' and len(mtext) > 3:
        teacher(event, mtext)
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))



def sendFlex(event):

    userId = event.source.user_id
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=userId+': '+event.message.text))

def student(event, mtext):
    try:
        flist = mtext[3:].split('/')
        # insert into students(sid,sname,sgrade,smajor,sdate,stime) values('B10702004','yang',3,'CS',current_date,localtime(0));
        if flist[0] == 'i':
            sql_cmd="insert into student (id,name,major,grade) values ('"+flist[1]+"','"+flist[2]+"','"+flist[3]+"','"+flist[4]+"');"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='insert complete!'))
        # elif flist[0] == 'u':
        #     sql_cmd="update students set sname='"+flist[2]+"',sgrade="+flist[3]+",smajor='"+flist[4]+"',sdate=current_date,stime=localtime(0) where sid = ('"+flist[1]+"');"
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='update complete！'))
        elif flist[0] == 'd':
            sql_cmd="delete from student where id =  '"+flist[1]+"';"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='delete complete！'))
        # elif flist[0] == 'q':
        #     sql_cmd="select * from students where sid = '"+flist[1]+"';"
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='search complete！'))
            
        db.engine.execute(sql_cmd)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def teacher(event, mtext):
    try:
        flist = mtext[3:].split('/')
        if flist[0] == 'i':
            sql_cmd="insert into teacher (id,name,major,grade) values ('"+flist[1]+"','"+flist[2]+"','"+flist[3]+"','"+flist[4]+"');"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='insert complete!'))
        elif flist[0] == 'd':
            sql_cmd="delete from teacher where id =  '"+flist[1]+"';"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='delete complete！'))

        db.engine.execute(sql_cmd)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def reschedule(event, mtext):
    try:
        flist = mtext[4:].split('/')
        # insert into students(sid,sname,sgrade,smajor,sdate,stime) values('B10702004','yang',3,'CS',current_date,localtime(0));
        if flist[0] == 'r':
            sql_cmd="update from student where id =  '"+flist[1]+"';"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='reschedule complete！'))
        # elif flist[0] == 'u':
        #     sql_cmd="update students set sname='"+flist[2]+"',sgrade="+flist[3]+",smajor='"+flist[4]+"',sdate=current_date,stime=localtime(0) where sid = ('"+flist[1]+"');"
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='update complete！'))
        elif flist[0] == 'c':
            sql_cmd="delete from student where id =  '"+flist[1]+"';"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='delete complete！'))
        # elif flist[0] == 'q':
        #     sql_cmd="select * from students where sid = '"+flist[1]+"';"
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='search complete！'))
            
        db.engine.execute(sql_cmd)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

if __name__=='__main__':
    app.run()
    
