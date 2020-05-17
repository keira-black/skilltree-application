
#!/usr/bin/env python3
from flask import Flask, jsonify, json, request, abort
import os
import psycopg2
#response = requests.get('https://httpbin.org/ip')
#print('Your IP is {0}'.format(response.json()['origin']))

app = Flask(__name__)

#DUMMY DATA
global userscount
userscount = 5

modules = [
	{
		'id': 1,
		'modulename': 'addition',
		'prerequisites':[]
	},
	{
		'id':2,
		'modulename': 'subtraction',
		'prerequisites':[
			{
				'id': 1, 
				'modulename': 'addition'
			}
		]
	}
]

#ToDo: remove creds, change creds
#dbconnstr: "dbname=skilltreedb user=postgres password=docker port=1000 host=172.17.0.1"
dbconnstr = os.environ["dbconnstr"]

#users
@app.route('/skilltree/api/v1.0/users', methods=['GET'])
def get_users():
	conn = psycopg2.connect(dbconnstr)
	cur = conn.cursor()
	cur.execute("select user_id, username, email, role from skilltree_backend.user")
	users = cur.fetchall()
	cur.close()
	usersjson = []
	for user in users:
		userjson = {'user_id': user[0], 'username': user[1], 'email': user[2], 'role': user[3]}
		usersjson.append(userjson)
	return jsonify({'users': usersjson})

@app.route('/skilltree/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    #user = [user for user in users if user['id'] == user_id]
	conn = psycopg2.connect(dbconnstr)
	cur = conn.cursor()
	#todo sanitize inputs
	cur.execute("select user_id, username, email, role from skilltree_backend.user where user_id="+str(user_id))
	user = cur.fetchone()
	cur.close()
	if len(user) == 0:
		abort(404)
	return jsonify({'user_id': user[0], 'username': user[1], 'email': user[2], 'role': user[3]})

@app.route('/skilltree/api/v1.0/users', methods=['POST'])
def create_user():
	content = request.get_json()
	try:
		conn = psycopg2.connect(dbconnstr)
		cur = conn.cursor()
		print(content['user_id'], content['username'], content['email'], content['password'], content['role'])
		cur.execute("""
			INSERT INTO skilltree_backend.user(user_id, username, email, password, role)
			VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);
			""", 
			(content['user_id'], content['username'], content['email'], content['password'], content['role']))
		conn.commit()
		cur.close()	
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"

    
	
@app.route('/skilltree/api/v1.0/users', methods=['PUT'])
def update_user(user_id):
	content = request.get_json()
	try:
		conn = psycopg2.connect(dbconnstr)
		cur = conn.cursor()
		cur.execute("""
			INSERT INTO skilltree_backend.user(user_id, username, email, password, role)
			VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);
			""", 
			(content['user_id'], content['username'], content['email'], content['password'], content['role']))
		conn.commit()
		cur.close()	
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(e.pgcode, e.content)
		return "failed to insert"
		
@app.route('/skilltree/api/v1.0/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	try:
		conn = psycopg2.connect(dbconnstr)
		cur = conn.cursor()
		cur.execute("DELETE FROM skilltree_backend.user WHERE user_id = CAST(%s AS BIGINT)", (user_id))
		conn.commit()
		cur.close()
	except psycopg2.Error as e:
		error = e.pgcode
		print(e.pgcode, e.content)

@app.route('/skilltree/doc/v1.0/users', methods=['GET'])
def get_users_doc():
	doc = """
		<html>
			<head>
				<title>/skilltree/doc/v1.0/users</title>
			</head>
			<body>
				<div style="border-radius: 5px; border: 1px solid black; background-color: cream; color: black; padding: 20px; margin: 20px">
					<h4>Get Users</h4>
					endpoint: /skilltree/api/v1.0/users<br>
					method: GET<br>
					description: returns a list of users
				</div>
				<div style="border-radius: 5px; border: 1px solid black; background-color: cream; color: black; padding: 20px; margin: 20px">
					<h4>Get User</h4>
					endpoint: /skilltree/api/v1.0/users/<b>userid</b><br>
					method: GET<br>
					description: returns a single user
				</div>
				<div style="border-radius: 5px; border: 1px solid black; background-color: cream; color: black; padding: 20px; margin: 20px">
					<h4>Create User</h4>
					endpoint: /skilltree/api/v1.0/users<br>
					method: POST<br>
					description: <br>
					creates a user. Expects:<br>
					<pre>
		{
			"username" : <b>username</b>(string),
			"isadmin" : (boolean)
		}
					</pre>
				</div>
			</body>
		</html>
	"""    
	return doc


#modules
@app.route('/skilltree/api/v1.0/modules', methods=['GET'])
def get_modules():
	conn = psycopg2.connect(dbconnstr)
	cur = conn.cursor()
	cur.execute("select module_id, name, description from skilltree_backend.module")
	modules = cur.fetchall()
	cur.close()
	modulesjson = []
	for module in modules:
		modulejson = {'module_id': module[0], 'name': module[1], 'description': module[2]}
		modulesjson.append(modulejson)
	return jsonify({'modules': modulesjson})


@app.route('/skilltree/api/v1.0/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
        #user = [user for user in users if user['id'] == user_id]
	conn = psycopg2.connect(dbconnstr)
	cur = conn.cursor()
	#todo sanitize inputs
	cur.execute("select module_id, name, description from skilltree_backend.module where module_id="+str(module_id))
	module = cur.fetchone()
	cur.close()
	if len(module) == 0:
		abort(404)
	return jsonify({'module_id': module[0], 'name': module[1], 'description': module[2]})


@app.route('/skilltree/api/v1.0/modules', methods=['POST'])
def create_module():
	content = request.get_json()
	try:
		conn = psycopg2.connect(dbconnstr)
		cur = conn.cursor()
		print(content['module_id'], content['name'], content['description'])
		cur.execute("""
			INSERT INTO skilltree_backend.module(module_id, name, description)
			VALUES (%s, %s, %s);
			""", 
			(content['module_id'], content['name'], content['description']))
		conn.commit()
		cur.close()	
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"
	
@app.route('/skilltree/api/v1.0/modules', methods=['PUT'])
def update_module():
	content = request.get_json()
	try:
		conn = psycopg2.connect(dbconnstr)
		cur = conn.cursor()
		cur.execute("""
			INSERT INTO skilltree_backend.module(module_id, name, description)
			VALUES (%s, %s, %s);
			""", 
			(content['module_id'], content['name'], content['description']))
		conn.commit()
		cur.close()	
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(e.pgcode, e.content)
		return "failed to insert"
		
@app.route('/skilltree/api/v1.0/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
	try:
		conn = psycopg2.connect(dbconnstr)
		cur = conn.cursor()
		cur.execute("DELETE FROM skilltree_backend.module WHERE module_id = CAST(%s AS BIGINT)", (module_id))
		conn.commit()
		cur.close()
	except psycopg2.Error as e:
		error = e.pgcode
		print(e.pgcode, e.content)

@app.route('/skilltree/doc/v1.0/modules', methods=['GET'])
def get_modules_doc():
	doc = """
		<html>
			<head>
				<title>/skilltree/doc/v1.0/modules</title>
			</head>
			<body>
				<div style="border-radius: 5px; border: 1px solid black; background-color: cream; color: black; padding: 20px; margin: 20px">
					<h4>Get Modules</h4>
					endpoint: /skilltree/api/v1.0/modules<br>
					method: GET<br>
					description: returns a list of modules
				</div>
				<div style="border-radius: 5px; border: 1px solid black; background-color: cream; color: black; padding: 20px; margin: 20px">
					<h4>Get Module</h4>
					endpoint: /skilltree/api/v1.0/modules/<b>moduleid</b><br>
					method: GET<br>
					description: returns a single module
				</div>

			</body>
		</html>
	"""    
	return doc

	

#execute application
if __name__ == '__main__':
	app.run(debug=True)
