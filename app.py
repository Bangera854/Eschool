from flask import Flask,render_template, request, redirect, session
import json
import os
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail

conn = mysql.connector.connect(host="localhost", user="root", password="home", database="sample")
cursor = conn.cursor()

with open("D:/Sandarsh/Rough/E school/template/config.json",'r') as c:
    param = json.load(c) ["param"]

local_server = True
app = Flask(__name__, template_folder='template')
app.secret_key = 'jvxrsjdsklj'
app.config.update(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = '465',
        MAIL_USE_SSL = True,
        MAIL_USERNAME = param['gmail_user'],
        MAIL_PASSWORD = param['gmail_pass']
)
mail = Mail(app)
#Uniform Resource Identifier
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:home@localhost/sample'

db = SQLAlchemy(app)

class Contacts(db.Model):
    s_no = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    phone = db.Column(db.Integer, unique = True, nullable = False)
    message = db.Column(db.String(120), unique = False, nullable = False)
    date = db.Column(db.String(12), unique = False, nullable = True, default = datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    uname = db.Column(db.String(80), unique = False, nullable = False)
    uemail = db.Column(db.String(120), unique = True, nullable = False)
    upass = db.Column(db.String(40), unique = False, nullable = False)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/course')
def courses():
    return render_template('course.html')

@app.route('/books')
def books():
    return render_template('books.html')



@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name = name,date = datetime.now(), phone = phone, email = email, message = message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from' + name, sender = email, recipients = [param['gmail_user']],
                          body = 'Message : ' + message + "\n" + 'phone no : ' + phone)

    return render_template('contact.html', param = param)



@app.route('/designv')
def designv():
    return render_template('designv.html')

@app.route('/biology')
def biology():
    return render_template('biology.html')

@app.route('/marketing')
def marketing():
    return render_template('marketing.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/physics')
def physics():
    return render_template('physics.html')

@app.route('/chemistry')
def chemistry():
    return render_template('chemistry.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/loginvalidation/', methods=['GET','POST'])
def loginvalidation():
    uname = request.form.get('uname')
    upass = request.form.get('upass')

    cursor.execute("""SELECT * FROM `users` WHERE `uname` LIKE '{}' AND `upass` LIKE '{}'"""
                    .format(uname,upass))
    users = cursor.fetchall()
    if len(users) > 0:
        return "<h2>User logged in <a href='/dashboard'>click here</a></h2>"
    else:
        return "<h2>Wrong details <a href='/login'>click here</a></h2>"


@app.route('/adduser', methods = ['POST'])
def add_user():
    uname=request.form.get('uname')
    uemail=request.form.get('uemail')
    upass=request.form.get('upass')
    session['uname'] = request.form['uname']
    cursor.execute("""INSERT INTO `users` (`id`, `uname`, `uemail`, `upass`) VALUES
    (NULL,'{}','{}','{}')""".format(uname,uemail,upass))
    if len(uname) > 0:
        conn.commit()
        return"<h2>User registered successfully, <a href='/login'>click here</a></h2>"
    else:
        return "<h2>Wrong details <a href='/signup'>click here</a></h2>"

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/dashboard')
def dashboard():
        return render_template('dashboard.html')

@app.route('/programming')
def programming():
    return render_template('Programming.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/cn')
def cn():
    return render_template('cn.html')

@app.route('/ml')
def ml():
    return render_template('ml.html')



if __name__ == "__main__":
    app.run(debug=True)