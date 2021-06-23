#!/usr/bin/python3

from dummy_actions import *
from flask import Flask, request
import json
import hashlib
from multiprocessing import Process
from RobopetFaceDetect.main import train
import os

hostileP = Process(target=dummy_hostile)
friendlyP = Process(target=dummy_friendly)
followP = Process(target=dummy_follow)
processes = [hostileP, friendlyP, followP]
app = Flask(__name__)


@app.route('/upload', methods=['PUT'])
def create_user():
    print("Got request")
    if 'video' not in request.files:
            print('No video available')
            print(request.files.keys())
            return "No video", 400

    username = request.form['user']
    user_id = int(hashlib.sha256(username.encode('utf-8')).hexdigest(), 16) % 10**8

    # read json file and update it
    # json file is a dict - key is ID (string), value is username
    with open("users.json", "r") as users_file:
        users_dict = json.loads(users_file.read().replace('\n', ''))
    if str(user_id) not in users_dict:
        users_dict[str(user_id)] = username
    with open("users.json", "w") as users_file:
        users_file.write(json.dumps(users_dict))

    f = request.files['video']
    path = f"videos/{username}"
    f.save(path)
    num_pics = train(user_id, path)
    if num_pics < 30:
        return str(num_pics), 422
    return str(num_pics), 201


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


@app.route('/follow', methods=['PUT'])
def follow():
    for p in processes:
        if p.is_alive():
            p.terminate()

    processes[2] = Process(target=dummy_follow)
    processes[2].start()
    return "OK", 204
