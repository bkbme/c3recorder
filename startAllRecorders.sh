#!/bin/bash
screen -dmS recorders ./hallRecorder.py 0
screen -S recorders -X screen 1 ./hallRecorder.py 1
screen -S recorders -X screen 2 ./hallRecorder.py 2
screen -S recorders -X screen 3 ./hallRecorder.py 3
screen -S recorders -X screen 4 ./hallRecorder.py 4
