#!/usr/bin/python3

from flask import Flask, request
app = Flask(__name__)

@app.route('/upload', methods=['PUT'])
def create_user():
	if 'picture' not in request.files:
		print('No picture available')
		print(request.files.keys())
		return "No picture", 400
	
	f = request.files['picture']
	f.save("1")
	return 201, "1"
