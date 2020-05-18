
#!/usr/bin/env python3
from flask import Flask, jsonify, json, request, abort
import os
import psycopg2
#response = requests.get('https://httpbin.org/ip')
#print('Your IP is {0}'.format(response.json()['origin']))

app = Flask(__name__)

#dbconnstr: "dbname=skilltreedb user=postgres password=docker port=1000 host=172.17.0.1"
dbconnstr = os.environ["dbconnstr"]

def dbExecute(queryStr, queryTuple):
	conn = psycopg2.connect(dbconnstr)
	cur = conn.cursor()
	cur.execute(queryStr, queryTuple)
	conn.commit()
	cur.close()

def fetchAll(queryStr):
	conn = psycopg2.connect(dbconnstr)
	cur = conn.cursor()
	cur.execute(queryStr)
	res = cur.fetchall()
	cur.close()
	return res

def fetchAllWithArgs(queryStr, queryTuple):
	conn = psycopg2.connect(dbconnstr)
	cur = conn.cursor()
	cur.execute(queryStr, queryTuple)
	res = cur.fetchall()
	cur.close()
	return res

def fetchOne(queryStr):
	conn = psycopg2.connect(dbconnstr)
	cur = conn.cursor()
	cur.execute(queryStr)
	res = cur.fetchone()
	cur.close()
	return res

#users
@app.route('/skilltree/api/v1.0/users', methods=['GET'])
def get_users():
	users = fetchAll("select user_id, username, email, role from skilltree_backend.user")
	usersjson = []
	for user in users:
		userjson = {'user_id': user[0], 'username': user[1], 'email': user[2], 'role': user[3]}
		usersjson.append(userjson)
	return jsonify({'users': usersjson})

@app.route('/skilltree/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    #user = [user for user in users if user['id'] == user_id]
	user = fetchOne("select user_id, username, email, role from skilltree_backend.user where user_id="+str(user_id))
	if len(user) == 0:
		abort(404)
	return jsonify({'user_id': user[0], 'username': user[1], 'email': user[2], 'role': user[3]})

@app.route('/skilltree/api/v1.0/users', methods=['POST'])
def create_user():
	content = request.get_json()
	try:
		dbExecute("""
			INSERT INTO skilltree_backend.user(user_id, username, email, password, role)
			VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);
			""", (content['user_id'], content['username'], content['email'], content['password'], content['role']))
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"
	
@app.route('/skilltree/api/v1.0/users', methods=['PUT'])
def update_user(user_id):
	content = request.get_json()
	try:
		dbExecute("""
			INSERT INTO skilltree_backend.user(user_id, username, email, password, role)
			VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);
			""", (content['user_id'], content['username'], content['email'], content['password'], content['role']))
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"
		
@app.route('/skilltree/api/v1.0/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	try:
		dbExecute("DELETE FROM skilltree_backend.user WHERE user_id = CAST(%s AS BIGINT)", (user_id))
		print("User with user id "+str(user_id)+" deleted.")
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
	modules = fetchAll("select module_id, name, description from skilltree_backend.module")
	modulesjson = []
	for module in modules:
		modulejson = {'module_id': module[0], 'name': module[1], 'description': module[2]}
		modulesjson.append(modulejson)
	return jsonify({'modules': modulesjson})

@app.route('/skilltree/api/v1.0/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
        #user = [user for user in users if user['id'] == user_id]
	module = fetchOne("select module_id, name, description from skilltree_backend.module where module_id="+str(module_id))
	if len(module) == 0:
		abort(404)
	return jsonify({'module_id': module[0], 'name': module[1], 'description': module[2]})

@app.route('/skilltree/api/v1.0/modules', methods=['POST'])
def create_module():
	content = request.get_json()
	try:
		dbExecute("""
			INSERT INTO skilltree_backend.module(module_id, name, description)
			VALUES (%s, %s, %s);
			""", 
			(content['module_id'], content['name'], content['description']))
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"
	
@app.route('/skilltree/api/v1.0/modules', methods=['PUT'])
def update_module():
	content = request.get_json()
	try:
		dbExecute("""
			INSERT INTO skilltree_backend.module(module_id, name, description)
			VALUES (%s, %s, %s);
			""", 
			(content['module_id'], content['name'], content['description']))
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"
		
@app.route('/skilltree/api/v1.0/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
	try:
		dbExecute("DELETE FROM skilltree_backend.module WHERE module_id = CAST(%s AS BIGINT)", (module_id))
		print("Succesful delete for module "+str(module_id))
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

@app.route('/skilltree/api/v1.0/prerequisites/<int:module_id>', methods=['GET'])
def get_prerequisites(module_id):
        #user = [user for user in users if user['id'] == user_id]
	prerequisites = fetchAll("select module_id, prerequisite_module_id from skilltree_backend.prerequisite where module_id="+str(module_id))
	if len(module) == 0:
		abort(404)
	return jsonify({'prerequisites': prerequisites })

@app.route('/skilltree/api/v1.0/prerequisites/<int:module_id>', methods=['POST'])
def create_prerequisite(module_id):
	content = request.get_json()
	try:
		dbExecute("""
			INSERT INTO skilltree_backend.user(module_id, prerequisite_module_id)
			VALUES (%s, %s);
			""", (content['module_id'], content['prerequisite_module_id']))
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"

@app.route('/skilltree/api/v1.0/prerequisites/<int:module_id>', methods=['PUT'])
def update_prerequisite(module_id):
	content = request.get_json()
	try:
		dbExecute("""
			INSERT INTO skilltree_backend.user(module_id, prerequisite_module_id)
			VALUES (%s, %s);
			""", (content['module_id'], content['prerequisite_module_id']))
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"

@app.route('/skilltree/api/v1.0/prerequisites', methods=['DELETE'])
def delete_prerequisite():
	content = request.get_json()
	try:
		module = content['module_id']
		prerequisite = content['prerequisite_module_id']
		dbExecute("DELETE FROM skilltree_backend.prerequisite WHERE module_id = CAST(%s AS BIGINT) AND prerequisite_module_id = CAST(%s AS BIGINT)", (module, prerequisite))
		print("Succesful delete for module "+str(module_id))
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to delete prerequisite"	

@app.route('/skilltree/api/v1.0/user_modules/<int:user_id>', methods=['GET'])
def get_user_module_relations(user_id):
	user_modules = fetchAllWithArgs("select module_id, progress from skilltree_backend.user_modules where user_id=CAST(%s AS BIGINT)",str(user_id))
	if len(user_modules) == 0:
		abort(404)
	return jsonify({'user_modules': user_modules })

@app.route('/skilltree/api/v1.0/prerequisites/<int:module_id>', methods=['POST'])
def relate_user_module(module_id):
	content = request.get_json()
	try:
		dbExecute("""
			INSERT INTO skilltree_backend.user_module(user_module_id, user_id, module_id, progress)
			VALUES (%s, %s, %s, %s);
			""", (content['user_module_id'], content['user_id'], content['module_id'], content['progress']))
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"

@app.route('/skilltree/api/v1.0/prerequisites/<int:module_id>', methods=['PUT'])
def update_user_module_relation(module_id):
	content = request.get_json()
	try:
		dbExecute("""
			INSERT INTO skilltree_backend.user_module(user_module_id, user_id, module_id, progress)
			VALUES (%s, %s, %s, %s);
			""", (content['user_module_id'], content['user_id'], content['module_id'], content['progress']))
		return "inserted succesfully"
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to insert"

@app.route('/skilltree/api/v1.0/user_modules', methods=['DELETE'])
def delete_user_module_relation():
	content = request.get_json()
	user = content['user_id']
	module = content['module_id']
	try:
		dbExecute("DELETE FROM skilltree_backend.user_module WHERE user_id = CAST(%s AS BIGINT) AND module_id = CAST(%s AS BIGINT)", (user, module))
		print("Succesful delete for user_module ")
	except psycopg2.Error as e:
		error = e.pgcode
		print(error.content)
		return "failed to delete user_module association"	

#execute application
if __name__ == '__main__':
	app.run(debug=True)
