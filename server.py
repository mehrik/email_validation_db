from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'maricIsAwesome'
mysql = MySQLConnector('emaildb')
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

@app.route('/')
def index():
	print '********** STARTED UP **********'
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
	email = request.form['email']

	if not EMAIL_REGEX.match(email) or len(email) < 1:
		flash('Email is not valid!')
		return redirect('/')

	query = "INSERT INTO emails (email_address, created_at)\
			VALUES ('{}', NOW())".format(request.form['email'])

	mysql.run_mysql_query(query)
	emailsdb = mysql.fetch('SELECT * FROM emails')
	return render_template('success.html', emailsdb=emailsdb, your_email=email)
	
app.run(debug=True)