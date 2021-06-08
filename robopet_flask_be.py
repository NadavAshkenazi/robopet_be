#!/usr/bin/python3

from dummy_actions import *
from flask import Flask, request
from multiprocessing import Process

hostileP = Process(target=dummy_hostile)
friendlyP = Process(target=dummy_friendly)
processes = [hostileP, friendlyP]
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

@app.route('/hostile', methods=['PUT'])
def hostile():
    for p in processes:
        if p.is_alive():
            p.terminate()

    processes[0] = Process(target=dummy_hostile)
    processes[0].start()
    return "OK", 204

@app.route('/friendly', methods=['PUT'])
def friendly():
    for p in processes:
        if p.is_alive():
            p.terminate()

    processes[1] = Process(target=dummy_friendly)
    processes[1].start()
    return "OK", 204

@app.route('/sleep', methods=['PUT'])
def sleep():
    for p in processes:
        if p.is_alive():
            p.terminate()

    return "OK", 204
