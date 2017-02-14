from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'FriendAssignment')
@app.route('/', methods=['GET'])
def index():
    friends = mysql.query_db("SELECT * FROM FriendsList")
    print friends
    return render_template('friends.html')
@app.route('/friends', methods=['POST'])
def create():

    query = "INSERT INTO FriendsList (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'email': request.form['email']
           }
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/friends/<id>', methods=['POST','GET'])
def show(friend_id):
    query = "UPDATE FriendsList SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'email': request.form['email'],
             'id': friend_id
           }
    mysql.query_db(query, data)
    return render_template('index.html', one_friend=friends[0])
@app.route('/friends/<id>/delete', methods=['POST'])
def delete(friend_id):
    friends = mysql.query_db("SELECT * FROM FriendsList")
    print friends
    query = "DELETE FROM FriendsList WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')
app.run(debug=True)
