from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
import os
from datetime import datetime
import datetime
import uuid
from werkzeug.utils import secure_filename
import random
from random import seed
from random import randint
from flask_mail import Mail, Message
from flask import send_file
import smtplib
import socket

import numpy as np
from matplotlib import pyplot as plt
import cv2
import threading
import os
import time
import shutil
import hashlib
import imagehash
import PIL.Image
from PIL import Image, ImageDraw, ImageFilter
import piexif

import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__, static_url_path='/static')
app.secret_key = 'abcdef'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    charset="utf8",
    use_pure=True,
    database="hall_allocate"
)


UPLOAD_FOLDER = 'static/hall'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


##email
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "exsample74@gmail.com",
    "MAIL_PASSWORD": "Exam12@exam"
}


scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval', minutes=1)
def delete_expired_rows():
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM hall_exam WHERE date < %s", (now,))
    mydb.commit()
    cursor.close()

scheduler.start()

app.config.update(mail_settings)
mail = Mail(app)


@app.route('/',methods=['POST','GET'])
def index():

    
    return render_template('index.html')


@app.route('/hod_reg',methods=['POST','GET'])
def hod_reg():


    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_dept")
    data1 = cursor.fetchall()
    cursor.close()

    msg=""
    if request.method=='POST':
        staff_type=request.form['staff_type']
        name=request.form['name']       
        mobile=request.form['mobile']
        email=request.form['email']
        dept=request.form['dept']
        address=request.form['address']
        staff_id=request.form['staff_id']
        password=request.form['password']
        now = datetime.datetime.now()
        r_date=now.strftime("%B %d, %Y")

                
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM hall_staff where staff_id=%s",(staff_id, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM hall_staff")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO hall_staff(id, staff_type, name, address, mobile, email, dept, staff_id, password, r_date) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s, %s)"
            val = (maxid, staff_type, name, address, mobile, email, dept, staff_id, password, r_date)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"
    
    return render_template('hod_reg.html', msg=msg, hall_dept=data1)


@app.route('/admin',methods=['POST','GET'])
def admin():
    
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor() 
        cursor.execute('SELECT * FROM hall_admin WHERE username = %s AND password = %s', (username, password))        
        admin = cursor.fetchone()
        cursor.close()
        if admin:
            session['username'] = username
            session['user_type'] = 'admin'
            msg = 'success'
            
        else:
            msg = 'fail'
            
    return render_template('admin.html', msg=msg)

@app.route('/hod_log',methods=['POST','GET'])
def hod_log():   

    msg=""
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        password = request.form['password']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM hall_staff WHERE staff_type="hod" AND staff_id = %s AND password = %s', (staff_id, password))
        account = cursor.fetchone()
        
        if account:
            session['staff_id'] = staff_id
            session['user_type'] = 'hod'
            msg="success"
            
        else:
            msg="fail"
            
    return render_template('hod_log.html', msg=msg)


@app.route('/staff_log',methods=['POST','GET'])
def staff_log():   

    msg=""
    
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        password = request.form['password']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM hall_staff WHERE staff_id = %s AND password = %s', (staff_id, password))
        account = cursor.fetchone()
        
        if account:
            session['staff_id'] = staff_id
            session['user_type'] = 'staff'
            msg="success"
            
        else:
            msg="fail"
            
    return render_template('staff_log.html', msg=msg)


@app.route('/add_exam',methods=['POST','GET'])
def add_exam():

    data2=""
    exam=""
    dept=""
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_dept")
    data1 = cursor.fetchall()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_exam1")
    data3 = cursor.fetchall()
    cursor.close()

    act=request.args.get("act")

    if act=="ok":
        exam=request.args.get("exam")
        dept=request.args.get("dept")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM hall_exam where exam_name=%s AND dept=%s", (exam, dept ))
        data2 = cursor.fetchall()
        cursor.close()

    msg=""
    if request.method=='POST':
        exam_name=request.form['exam_name']
        sub_name=request.form['sub_name']       
        sub_code=request.form['sub_code']
        date=request.form['date']
        dept=request.form['dept']
        semester=request.form['semester']
        now = datetime.datetime.now()
        r_date=now.strftime("%B %d, %Y")

                
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM hall_exam where sub_name=%s",(sub_name, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM hall_exam")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO hall_exam(id, exam_name, sub_name, sub_code, date, dept, semester, r_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, exam_name, sub_name, sub_code, date, dept, semester, r_date)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"
        
        
            
    return render_template('add_exam.html', msg=msg, hall_exam=data2, hall_exam1=data3, hall_dept=data1, exam=exam, dept=dept)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_hall',methods=['POST','GET'])
def add_hall():

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_dept")
    data1 = cursor.fetchall()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_hall")
    data2 = cursor.fetchall()
    cursor.close()

    act=request.args.get('act')
    if act=="ok":
        eid=request.args.get('eid')
        cursor = mydb.cursor()
        cursor.execute('delete from hall_hall WHERE id = %s', (eid, ))
        mydb.commit()
        cursor.close()

    msg=""
    if request.method=='POST':
        hall_name=request.form['hall_name']
        capacity=request.form['capacity']       
        dept=request.form['dept']
        now = datetime.datetime.now()
        r_date=now.strftime("%B %d, %Y")
        
        mycursor = mydb.cursor()

                
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM hall_hall where hall_name=%s",(hall_name, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM hall_hall")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO hall_hall(id, hall_name, capacity, dept, r_date) VALUES (%s, %s, %s, %s, %s)"
            val = (maxid, hall_name, capacity, dept, r_date)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"
            
    return render_template('add_hall.html', msg=msg, hall_dept=data1, hall_hall=data2)



@app.route('/add_dept',methods=['POST','GET'])
def add_dept():

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_dept")
    data2 = cursor.fetchall()
    cursor.close()

    act=request.args.get('act')
    if act=="ok":
        eid=request.args.get('eid')
        cursor = mydb.cursor()
        cursor.execute('delete from hall_dept WHERE id = %s', (eid, ))
        mydb.commit()
        cursor.close()

    msg=""
    if request.method=='POST':
        dept=request.form['dept']
        now = datetime.datetime.now()
        r_date=now.strftime("%B %d, %Y")

                
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM hall_dept where dept=%s",(dept, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM hall_dept")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO hall_dept(id, dept, r_date) VALUES (%s, %s, %s)"
            val = (maxid, dept, r_date)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"
            
    return render_template('add_dept.html', msg=msg, hall_dept=data2)


@app.route('/add_exam2',methods=['POST','GET'])
def add_exam2():

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_dept")
    data1 = cursor.fetchall()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_exam1")
    data2 = cursor.fetchall()
    cursor.close()

    act=request.args.get('act')

    if act=="ok":
        eid=request.args.get('eid')
        cursor = mydb.cursor()
        cursor.execute('delete from hall_exam1 WHERE id = %s', (eid, ))
        mydb.commit()
        cursor.close()

    msg=""
    if request.method=='POST':
        exam_name=request.form['exam_name']
        dept=request.form['dept']
        now = datetime.datetime.now()
        r_date=now.strftime("%B %d, %Y")

                
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM hall_exam1 where exam_name=%s",(exam_name, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM hall_exam1")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO hall_exam1(id, exam_name, r_date, dept) VALUES (%s, %s, %s, %s)"
            val = (maxid, exam_name, r_date, dept)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"
            return redirect(url_for('add_exam'))
            
        else:
            msg="fail"
            
    return render_template('add_exam2.html', msg=msg, hall_exam1=data2, hall_dept=data1)



@app.route('/update',methods=['POST','GET'])
def update():


    if request.method=='POST':
        hall_name=request.form['hall_name']
        capacity=request.form['capacity']
        
        aid=request.form['aid']
        cursor = mydb.cursor()
        cursor.execute("UPDATE hall_hall SET hall_name=%s, capacity=%s WHERE id=%s", (hall_name, capacity, aid))
        mydb.commit()
        mycursor.close()
        
            
    return redirect(url_for('add_hall'))


@app.route('/hod_view',methods=['POST','GET'])
def hod_view():
    if 'staff_id' not in session or session.get('user_type') != 'hod':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('hod_log'))
    staff=""
    
    staff_id = session.get('staff_id')

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_id=%s",(staff_id, ))
    data = cursor.fetchone()
    cursor.close()
    dept=data[6]
    staff=data[2]

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_type='staff' and dept=%s",(dept, ))
    data1 = cursor.fetchall()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_hall where dept=%s",(dept, ))
    data2 = cursor.fetchall()
    cursor.close()

   
            
    return render_template('hod_view.html', hall_hall=data2, hall_staff=data1, staff=staff)


@app.route('/hod_exam',methods=['POST','GET'])
def hod_exam():
    if 'staff_id' not in session or session.get('user_type') != 'hod':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('hod_log'))

    staff_id = session.get('staff_id')
    data2=""
    dat=""
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_id=%s",(staff_id, ))
    data = cursor.fetchone()
    cursor.close()
    dept=data[6]
    staff=data[2]

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_exam1 where dept=%s",(dept, ))
    data1 = cursor.fetchall()
    cursor.close()

    act=request.args.get("act")
    exam=request.args.get("exam")
    dept=request.args.get("dept")

    if act=="ok":
        
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM hall_exam where exam_name=%s AND dept=%s", (exam, dept ))
        data2 = cursor.fetchall()
        cursor.close()

    if request.method=='POST':
        search=request.form['search']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM hall_exam where semester=%s AND exam_name=%s AND dept=%s", (search, exam, dept ))
        data2 = cursor.fetchall()
        cursor.close()

    return render_template('hod_exam.html', hall_exam1=data1, hall_exam=data2)

@app.route('/hod_allocate',methods=['POST','GET'])
def hod_allocate():
    if 'staff_id' not in session or session.get('user_type') != 'hod':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('hod_log'))

    staff_id = session.get('staff_id')
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_id=%s",(staff_id, ))
    data = cursor.fetchone()
    cursor.close()
    dept=data[6]
    staff=data[2]
    email=data[4]


    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_type='staff' and dept=%s",(dept, ))
    data1 = cursor.fetchall()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_hall where dept=%s",(dept, ))
    data2 = cursor.fetchall()
    cursor.close()

    act=request.args.get("act")
    act1=request.args.get("act1")
    act2=request.args.get("act2")

    now = datetime.datetime.now()
    r_date=now.strftime("%B %d, %Y")

    if act == "ok":
        suid = request.args.get("suid")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM hall_exam where id=%s", (suid,))
        data21 = cursor.fetchone()
        cursor.close()
        sub_code = data21[2]
        sub_name = data21[3]
        date = data21[6]
        semester=data21[5]

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM hall_allocate")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO hall_allocate(id, sub_code, sub_name, date, r_date, staff_id, hod_name, semester) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, sub_code, sub_name, date, r_date, staff_id, staff, semester)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        
        session['maxid'] = maxid  # Store maxid in session
        return redirect(url_for('hod_allocate1'))

    cursor = mydb.cursor()
    cursor.execute("SELECT DISTINCT hall_name FROM hall_allocate")
    allocated_reg_nos = [row[0] for row in cursor.fetchall()]
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT DISTINCT staff_user FROM hall_allocate")
    allocated_reg_no = [row[0] for row in cursor.fetchall()]
    cursor.close()
            
    return render_template('hod_allocate.html', hall_hall=data2, hall_staff=data1, staff=staff, msg=msg, allocated_reg_nos=allocated_reg_nos, allocated_reg_no=allocated_reg_no)


@app.route('/hod_allocate1',methods=['POST','GET'])
def hod_allocate1():
    if 'staff_id' not in session or session.get('user_type') != 'hod':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('hod_log'))

    act=""
    st=""
    hall_name=""
    email=""
    staff=""
    link=""
    mess=""
    
    sm=""
    maxid = session.get('maxid')

    hall_name=""
    staff_user=""
    
    staff_id = session.get('staff_id')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_id=%s",(staff_id, ))
    data = cursor.fetchone()
    cursor.close()
    dept=data[6]
    staff=data[2]

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_type='staff' and dept=%s", (dept,))
    data1 = cursor.fetchall()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_hall where dept=%s", (dept,))
    data2 = cursor.fetchall()
    cursor.close()

    act = request.args.get('act')
    act2 = request.args.get('act2')

    if act == "ok":
        hid = request.args.get("hid")
   
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM hall_hall where id=%s", (hid,))
        data22 = cursor.fetchone()
        cursor.close()
        hall_name = data22[1]
        hall_image = data22[4]
        cursor = mydb.cursor()
        cursor.execute("UPDATE hall_allocate SET hall_name=%s, hall_image=%s WHERE id=%s", (hall_name, hall_image, maxid))
        mydb.commit()
        cursor.close()
        msg="success1"
        
    else:
        msg="fail1"
    
    if act2 == "no":
        sid = request.args.get("sid")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM hall_staff where id=%s", (sid,))
        data23 = cursor.fetchone()
        cursor.close()
        staff_name = data23[2]
        staff_user = data23[7]
        staff_email = data23[3]
        staff_mobile = data23[4]
        
        

        cursor = mydb.cursor()
        cursor.execute("UPDATE hall_allocate SET staff_name=%s, staff_user=%s, staff_email=%s, staff_mobile=%s WHERE id=%s", (staff_name, staff_user, staff_mobile, staff_email, maxid))
        mydb.commit()
        msg="success2"

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM hall_allocate where id=%s", (maxid, ))
        da = cursor.fetchone()
        cursor.close()
        staff=da[6]
        email=da[8]
        hall_name=da[4]

        link = "https://geobits.onrender.com/"

        msg = "success"
            
        mess = f"Reminder:Hi {staff}, Your Hall is {hall_name} click to check {link}"

        st="1"


    
    cursor = mydb.cursor()
    cursor.execute("SELECT DISTINCT hall_name FROM hall_allocate")
    allocated_reg_nos = [row[0] for row in cursor.fetchall()]
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT DISTINCT staff_user FROM hall_allocate")
    allocated_reg_no = [row[0] for row in cursor.fetchall()]
    cursor.close()

            
    return render_template('hod_allocate1.html', hall_hall=data2, hall_staff=data1, hall_name=hall_name, staff_user=staff_user, maxid=maxid, staff=staff, allocated_reg_nos=allocated_reg_nos, allocated_reg_no=allocated_reg_no, mess=mess, st=st, link=link, email=email)


@app.route('/allot_details',methods=['POST','GET'])
def allot_details():
    if 'staff_id' not in session or session.get('user_type') != 'hod':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('hod_log'))

    staff_id = session.get('staff_id')

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_allocate WHERE staff_id=%s ORDER BY semester ASC", (staff_id,))
    data2 = cursor.fetchall()
    cursor.close()

    act=request.args.get('act')
    if act=="ok":
        aid=request.args.get('aid')
        cursor = mydb.cursor()
        cursor.execute("delete from hall_allocate where id=%s",(aid,))
        mydb.commit()

    if act=="no":
        aid=request.args.get('aid')
        cursor = mydb.cursor()
        cursor.execute("update hall_allocate set changee=3 where id=%s ",(aid,))
        mydb.commit()

    return render_template('allot_details.html', hall_allocate=data2)


@app.route('/staff_view',methods=['POST','GET'])
def staff_view():
    if 'staff_id' not in session or session.get('user_type') != 'staff':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('staff_log'))

    staff_id = session.get('staff_id')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_id=%s",(staff_id, ))
    data = cursor.fetchone()
    cursor.close()
    staff=data[2]
    dept=data[6]

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff where staff_type='hod' AND dept=%s",(dept, ))
    data1 = cursor.fetchone()
    cursor.close()
    staff_name=data1[2]
    mobile=data1[3]
    email=data1[4]

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_staff WHERE staff_id=%s", (staff_id,))
    data2 = cursor.fetchone()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_exam where dept=%s", (dept, ))
    dataa = cursor.fetchall()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_allocate WHERE staff_user=%s", (staff_id,))
    data5 = cursor.fetchone()
    cursor.close()

    act=request.args.get('act')
    if act=="ok":
        aid=request.args.get('aid')
        cursor = mydb.cursor()
        cursor.execute("update hall_allocate set changee=1 where id=%s ",(aid,))
        mydb.commit()
        

    return render_template('staff_view.html', data2=data2, staff=staff, hall_exam=dataa, data5=data5, staff_name=staff_name, mobile=mobile, email=email)


@app.route('/edit',methods=['POST','GET'])
def edit():


    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        aid=request.form['aid']
        cursor = mydb.cursor()
        cursor.execute("UPDATE hall_staff SET name=%s, mobile=%s, email=%s, address=%s WHERE id=%s", (name, mobile, email, address, aid))
        mydb.commit()
        mycursor.close()
        
            
    return redirect(url_for('staff_view'))


@app.route('/report',methods=['POST','GET'])
def report():
    if 'staff_id' not in session or session.get('user_type') != 'staff':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('staff_log'))

    staff_id = session.get('staff_id')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hall_allocate where staff_id=%s",(staff_id, ))
    data2 = cursor.fetchall()

    return render_template('report.html', hall_allocate=data2)



@app.route('/logout')
def logout():
    
    session.clear()
    print("Logged out successfully", 'success')
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)

