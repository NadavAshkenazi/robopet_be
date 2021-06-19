#!/usr/bin/python3

from dummy_actions import *
from flask import Flask, request
from multiprocessing import Process

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
    
    print("files:")
    for k in request.files.keys():
        print(k)
    print("args:")
    for k in request.args.keys():
        print(k)
    print("form:")
    for k in request.form.keys():
        print(k)
    f = request.files['video']
    f.save(f"videos/{request.form['user']}")
    return "1", 201

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
