#!/bin/bash
source `which virtualenvwrapper.sh`
workon cv

#export PYTHONPATH="~/RobopetFaceDetect/:$PYTHONPATH"
export FLASK_APP=robopet_flask_be.py
flask run -h 0.0.0.0 -p 3000 > ~/log.txt 2>&1 &
