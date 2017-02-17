from flask import Flask, render_template, request, redirect, flash,session
import re
from flask.ext.bcrypt import Bcrypt
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "key"
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'thewalldb')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile('[a-zA-Z]+$')

@app.route('/',methods=['GET'])
def hompage():
    return render_template('logandregi.html')
@app.route('/wall', methods=['POST'])
def log():
    query = "SELECT password FROM users WHERE email = '{}'".format(request.form['l_email'])
    info = mysql.query_db(query)
    errors = False
    email = request.form['l_email']

    if len(email) < 1:
        flash("Email cannot be blank!")
        errors = True
        return redirect('/')
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!")
        errors = True
        return redirect('/')
    if not bcrypt.check_password_hash(info[0]["password"], request.form['l_pwd']):
        flash("Email or Password is not correct")
        erorrs = True
        return redirect('/')
    if errors == False:
        if bcrypt.check_password_hash(info[0]["password"], request.form['l_pwd']):
            query2 = "SELECT id, first_name FROM users WHERE email = '{}'".format(request.form['l_email'])
            user = mysql.query_db(query2)
            session["ID"] = user[0]["id"]
            session["firstname"] = user[0]["first_name"]
            return redirect('/home')

@app.route('/home',methods=['GET'])
def home():
    query = "SELECT messages.id, messages.message, messages.users_id, messages.created_at, users.first_name, users.last_name from messages join users on users.id = messages.users_id order by messages.created_at DESC"
    msg = mysql.query_db(query)

    query2 = "SELECT comments.id,comments.messages_id, messages.id, comments.comment,comments.users_id, comments.created_at, users.first_name, users.last_name from comments join users on users.id = comments.users_id join messages on messages.id = comments.messages_id order by comments.created_at DESC;"
    comment = mysql.query_db(query2)

    return render_template('homepage.html', message=msg, comment=comment)
@app.route('/regi', methods=['POST','GET'])
def regi2():
    return render_template('regiform.html')

@app.route('/regi/form', methods=['POST'])
def register():
    errors = False
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm']
    pw_hash = bcrypt.generate_password_hash(password)

    if len(fname) < 2:
        flash("First name should be at least 2 characters")
        errors = True
    elif not NAME_REGEX.match(fname):
        flash("First Name should be letter")
        errors = True
    if len(lname) < 2:
        flash("Last name should be at least 2 characters")
        errors = True
    elif not NAME_REGEX.match(lname):
        flash("First Name should be letter")
        errors = True
    if len(email) < 1:
        flash("Email cannot be blank!")
        errors = True
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!")
        errors = True
    if len(password) < 8:
        flash("password should be at least 8 characters")
        errors = True
    if password!= confirm:
        flash("password is not matched")
        errors = True

    if errors == True:
        return redirect('/regi')

    if errors == False:
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
        data = {
                 'first_name': fname,
                 'last_name':  lname,
                 'email': email,
                 'password' : pw_hash
               }
        mysql.query_db(query, data)
        flash("You are successfully regiestered")
        return redirect('/')
@app.route('/logout',methods=['POST'])
def logout():
    session.clear()
    return redirect('/')
@app.route('/msgpost',methods=['POST'])
def postmsg():
    errors = False
    msg = request.form['msg']

    if len(msg)< 1:
        flash("Message should not be blank")
        error = True
        return redirect('/home')
    if errors == False:
        query = "INSERT INTO messages (message, users_id, created_at, updated_at) VALUES (:newmessage,:user_id,now(),now())"
        data ={
        'newmessage' : request.form['msg'],
        'user_id' : session['ID']
        }
        mysql.query_db(query, data)
        flash("Your message is posted")
        return redirect('/home')
@app.route('/comment/<MessageID>',methods=['POST','GET'])
def commnet(MessageID):
    errors = False
    comment = request.form['commentino']

    if len(comment)< 1:
        flash("Comment should not be blank")
        error = True
        return redirect('/home')
    if errors == False:
        query = "INSERT INTO comments (comment, users_id, messages_id, created_at, updated_at) VALUES (:newcomment, :user_id, :message_id,  now(),now())"
        data ={
        'newcomment' : request.form['commentino'],
        'user_id' : session['ID'],
        'message_id' : MessageID
        }
        mysql.query_db(query, data)
        flash("Your comment is posted")
        return redirect('/home')
app.run(debug=True)
