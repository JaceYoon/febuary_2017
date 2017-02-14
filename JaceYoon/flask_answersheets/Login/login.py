from flask import Flask, render_template, request, redirect, flash,session
import re
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "key"

mysql = MySQLConnector(app, 'thewalldb')


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile('[a-zA-Z]+$')

@app.route('/',methods=['POST','GET']) #main page
def survey():
    return render_template('homepage.html')

@app.route('/login', methods=['POST','GET']) #msg showing page
def log():
    l_email = request.form['l_email']
    l_pwd = request.form['l_pwd']
    info = mysql.query_db("select email,pwd from users")

    for key in info:
        if key['email'] == l_email and key['pwd']== l_pwd:
            flash("You are successfully logged in! welcome back")
            return render_template('/')
    else:
        flash("Your email or password is not correct")
        return render_template('/login')


@app.route('/regi', methods=['POST','GET']) #regiester page
def regi2():
    return render_template('regiform.html')

@app.route('/regi/form', methods=['POST']) #regiester function
def go2():
    errors = False
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    pwd = request.form['pwd']
    confirm = request.form['confirm']

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
    if len(pwd) < 8:
        flash("password should be at least 8 characters")
        errors = True
    if pwd!= confirm:
        flash("password is not matched")
        errors = True

    if errors == True:
        return redirect('/regi')

    if errors == False:
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at, pwd) VALUES (:first_name, :last_name, :email, NOW(), NOW(), :pwd)"
        data = {
                 'first_name': request.form['fname'],
                 'last_name':  request.form['lname'],
                 'email': request.form['email'],
                 'pwd' : request.form['pwd']
               }
        mysql.query_db(query, data)
        flash("You are successfully regiestered")
        return redirect('/homepage')

app.run(debug=True)
