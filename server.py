from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from datetime import datetime
import re
app = Flask(__name__)
app.secret_key = 'maricIsAwesome'
mysql = MySQLConnector('emaildb')
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
	email = request.form['email']
	if not EMAIL_REGEX.match(email) or len(email) < 1:
		flash('Email is not valid!')
		return redirect('/')
	# Inserting email address into the database
	query = "INSERT INTO emails (email_address, created_at)\
			VALUES ('{}', NOW())".format(email)
	mysql.run_mysql_query(query)
	emailsdb = mysql.fetch('SELECT * FROM emails')
	return render_template('success.html', emailsdb=emailsdb, \
		your_email=email, message='insert')

@app.route('/delete', methods=['POST'])
def delete():
	email_id = request.form['delete']
	deleted_email = request.form['deleted_email']
	# Deleting email address from the database
	query = "DELETE FROM `emaildb`.`emails` WHERE `id`='{}'".format(email_id)
	mysql.run_mysql_query(query)
	emailsdb = mysql.fetch('SELECT * FROM emails')
	return render_template('success.html', emailsdb=emailsdb, \
		deleted_email=deleted_email, message='delete')

app.run(debug=True)