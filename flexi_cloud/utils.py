import sqlite3 as sql
from os import listdir

def encrypt(password):
	e_pass=''
	for i in password:
		e_pass+=chr(ord(i)+7)
	return e_pass

def decrypt(password):
	e_pass=''
	for i in password:
		e_pass+=chr(ord(i)-7)
	return e_pass

def update_db(data): # data = [username, email, password-encrypted]
	with sql.connect('./static/flexi.db') as conn:
		cur = conn.cursor()
		cur.execute(f'insert into users values("{data[0]}","{data[1]}","{data[2]}","{data[3]}")')
		cur.close()

def is_unique_user(user,email):
	with sql.connect('./static/flexi.db') as conn:
		cur = conn.cursor()
		data = cur.execute(f'select username, email from users where username="{user}" and email="{email}"')
		data = data.fetchall()
		cur.close()
		if len(data)!=0:
			return 0
		else:
			return 1

def change_passwd(user,passwd):
	with sql.connect('./static/flexi.db') as conn:
		cur = conn.cursor()
		data = cur.execute(f'update users set password="{encrypt(passwd)}" where username="{user}"')
		cur.close()

def user_check(username, password):
	conn = sql.connect('./static/flexi.db')
	cur = conn.cursor()
	users = cur.execute(f'select username, password, fullname from users where username="{username}"')
	users = users.fetchall()
	cur.close()
	conn.close()
	if len(users)==0:
		return "The username is not registered with our records. Please Sign Up to use the service."

	elif password and users[0][1]!=encrypt(password):
		return "The password you enterd was incorrect. Try again"
	else:
		return [1, users[0][-1].split()[0], users[0][0]]

def get_files(user):
	if user in listdir(f'./storage/'):
		file_list = listdir(f'./storage/{user}')
		return file_list
	else:
		return None
