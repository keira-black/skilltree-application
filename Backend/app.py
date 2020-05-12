
#!/usr/bin/env python3
from flask import Flask, jsonify, json, request, abort
#response = requests.get('https://httpbin.org/ip')
#print('Your IP is {0}'.format(response.json()['origin']))

app = Flask(__name__)

#DUMMY DATA
global userscount
userscount = 2
users = [
    {
        'id': 1,
        'username': 'jessicarabbit',
        'isadmin' : True
    },
    {
        'id': 2,
        'username': 'captaintripps',
        'isadmin' : False
    }
]

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

#users
@app.route('/skilltree/api/v1.0/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.route('/skilltree/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

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

@app.route('/skilltree/api/v1.0/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	
	return jsonify({'users': users})

@app.route('/skilltree/api/v1.0/users/')

#modules
@app.route('/skilltree/api/v1.0/modules', methods=['GET'])
def get_modules():
    return jsonify({'modules': modules})


@app.route('/skilltree/api/v1.0/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
    module = [module for module in modules if module['id'] == module_id]
    if len(module) == 0:
        abort(404)
    return jsonify({'module': module[0]})

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
