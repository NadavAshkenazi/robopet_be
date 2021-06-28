#!/usr/bin/python3

from behaviors import _bark, _spin
from behaviors import *
from flask import Flask, request
import json
import hashlib
from multiprocessing import Process
from picamera import PiCamera
from RobopetFaceDetect.main import train
from robopetSerial import mySerial

hostileP = None
friendlyP = None
processes = [hostileP, friendlyP]
app = Flask(__name__)


@app.route('/take_video', methods=['PUT'])
def record_user():
    print("Got request")

    ser = mySerial()
    ser.init_serial()
    print("cam_setY 90")
    ser.write("cam_setY 90")
    time.sleep(0.5)

    username = request.form['user']
    user_id = int(hashlib.sha256(username.encode('utf-8')).hexdigest(), 16) % 10**8

    # read json file and update it
    # json file is a dict - key is ID (string), value is username
    try:
        with open("users.json", "r") as users_file:
            users_dict = json.loads(users_file.read().replace('\n', ''))
    except:
        users_dict = {}
    if str(user_id) not in users_dict:
        users_dict[str(user_id)] = username
    with open("users.json", "w") as users_file:
        users_file.write(json.dumps(users_dict))

    path = f"videos/{username}.h264"
    camera = PiCamera()
    camera.rotation = 270
    camera.start_recording(path)
    time.sleep(8)
    camera.stop_recording()

    num_pics = train(user_id, path)
    if num_pics < 30:
        return str(num_pics), 422
    return str(num_pics), 201


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
    try:
        with open("users.json", "r") as users_file:
            users_dict = json.loads(users_file.read().replace('\n', ''))
    except:
        users_dict = {}
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
    for i, p in enumerate(processes):
        if p is not None and p.is_alive():
            p.terminate()
            processes[i] = None

    processes[0] = Process(target=behave_hostile)
    processes[0].start()
    return "OK", 204


@app.route('/friendly', methods=['PUT'])
def friendly():
    for i, p in enumerate(processes):
        if p is not None and p.is_alive():
            p.terminate()
            processes[i] = None

    processes[1] = Process(target=behave_friendly)
    processes[1].start()
    return "OK", 204


@app.route('/sleep', methods=['PUT'])
def sleep():
    for p in processes:
        if p.is_alive():
            p.terminate()

    return "OK", 204


# @app.route('/follow', methods=['PUT'])
# def follow():
#     for p in processes:
#         if p.is_alive():
#             p.terminate()
#
#     processes[2] = Process(target=behave_follow)
#     processes[2].start()
#     return "OK", 204



@app.route('/bark', methods=['PUT'])
def bark():
    _bark()
    return "OK", 204


@app.route('/wag', methods=['PUT'])
def wag():
    ser = mySerial()
    ser.init_serial()
    for i in range(4):
        ser.write("shakeTail")
        time.sleep(0.2)
    return "OK", 204



@app.route('/spin', methods=['PUT'])
def spin():
    _spin()
    return "OK", 204
