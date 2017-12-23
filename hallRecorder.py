#!/usr/bin/python3
import sys
from c3recorder import TalkRecorder
import time
import constants

room = constants.rooms[int(sys.argv[1])]
destDir = constants.videoDestDir + room + '/'
saal = TalkRecorder(room, destDir)

print("Starting recorder for room {} to save in {} ...".format(room, destDir))

while True:
  saal.poll()
  for i in range(60):
    saal.pollSecond()
    time.sleep(1)
