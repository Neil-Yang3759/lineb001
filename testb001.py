# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:43:39 2021

@author: cloud
"""
from flask import request,abort,render_template,Flask,redirect,url_for
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
liffid3 = '1655833971-10qjl0re'
liffid4 = '1655833971-MOY5bOva'

@app.route('/page1')
def page1():
	return render_template('student.html', liffid = liffid1)
@app.route('/page2')
def page2():
	return render_template('reschedule.html', liffid = liffid2)
@app.route('/page3')
def page3():
	return render_template('teacher.html', liffid = liffid3)
@app.route('/page4')
def page4():
	return render_template('query.html', liffid = liffid4)

@app.route('/post_student',methods=['POST'])            #post_student profile
def post_student():
    id = request.form['id']
    name = request.form['name']  
    major = request.form['major']
    grade = request.form['grade']
    strSQl= "insert into student values('"+id+"','"+name+"','"+major+"','"+grade+"');"
    db.engine.execute(strSQl) 
    return redirect(url_for('success'))

@app.route('/update_student',methods=['POST'])          #update_student profile
def update_student():
    id = request.form['id']
    name = request.form['name']  
    major = request.form['major']
    grade = request.form['grade']
    strSQl= "update student set name='"+name+"', major='"+major+"', grade='"+grade+"' where id='"+id+"'";
    db.engine.execute(strSQl) 
    return redirect(url_for('success'))

@app.route('/post_teacher',methods=['POST'])            #post_teacher profile
def post_teacher():
    id = request.form['id']
    name = request.form['name']  
    major = request.form['major']
    grade = request.form['grade']
    strSQl= "insert into teacher values('"+id+"','"+name+"','"+major+"','"+grade+"' );"
    db.engine.execute(strSQl) 
    return redirect(url_for('success'))

@app.route('/update_teacher',methods=['POST'])          #update_teacher profile
def update_teacher():
    id = request.form['id']
    name = request.form['name']  
    major = request.form['major']
    grade = request.form['grade']
    strSQl= "update teacher set name='"+name+"', major='"+major+"', grade='"+grade+"'  where id='"+id+"'";
    db.engine.execute(strSQl) 
    return redirect(url_for('success'))

@app.route('/success')                  #after you enter your profile correctly 
def success():
    return render_template('success.html')

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
    # elif mtext[:3] == '###' and len(mtext) > 3:
    #     reschedule(event, mtext)
    elif mtext[:4] == '####' and len(mtext) > 4:
        reschedule(event, mtext)
    # elif mtext[:3] == '##$' and len(mtext) > 3:
    #     teacher(event, mtext)
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


def sendFlex(event):

    userId = event.source.user_id
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=userId+': '+event.message.text))


def reschedule(event, mtext):               #reschedule and cancel class
    try:
        flist = mtext[4:].split('/')
        if flist[0] == 'r':
            sql_cmd="insert into public."+'"'+flist[8]+'"'+" select date,id,teacher,start_time,end_time,tlid from public."+'"'+flist[4]+'"'+" where date =  '"+flist[1]+"' and start_time = "+flist[2]+" and end_time = "+flist[3]+";"
            sql_cmd+="update public."+'"'+flist[8]+'"'+" set date = '"+flist[5]+"', start_time = "+flist[6]+", end_time = "+flist[7]+";"
            sql_cmd+="delete from public."+'"'+flist[4]+'"'+" where date =  '"+flist[1]+"' and start_time = "+flist[2]+" and end_time = "+flist[3]+";"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='reschedule complete！'))
        elif flist[0] == 'c':
            sql_cmd="delete from public."+'"'+flist[4]+'"'+" where date =  '"+flist[1]+"' and start_time = "+flist[2]+" and end_time = "+flist[3]+";"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='delete complete！'))

        db.engine.execute(sql_cmd)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

@app.route('/calendar_Room', methods=['GET','POST'])
def calendar_Room():
    class Room(db.Model):
        __tablename__ = request.form['room']
        __table_args__ = {'extend_existing': True}
        date = db.Column(db.Date,primary_key=True)
        id = db.Column(db.String)
        name = db.Column(db.String)
        teacher = db.Column(db.String)
        start_time = db.Column(db.Time,primary_key=True)
        end_time = db.Column(db.Time,primary_key=True)
        tlid = db.Column(db.String)
        room = db.Column(db.String)

    Rooms = Room.query.all()
    return render_template('calendar_Room.html',Rooms=Rooms)

@app.route('/calendar_Teacher', methods=['GET','POST'])
def calendar_Teacher():
    class Teacher_course(db.Model):
        __tablename__ = request.form['teacher']+"_course"
        __table_args__ = {'extend_existing': True}
        date = db.Column(db.Date,primary_key=True)
        id = db.Column(db.String)
        name = db.Column(db.String)
        teacher = db.Column(db.String)
        start_time = db.Column(db.Time,primary_key=True)
        end_time = db.Column(db.Time,primary_key=True)
        tlid = db.Column(db.String)
        room = db.Column(db.String)

    Teacher = Teacher_course.query.all()
    return render_template('calendar_Teacher.html',Teacher=Teacher)

if __name__=='__main__':
    app.run()