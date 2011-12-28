#!/usr/bin/python3
from c3recorder import TalkRecorder
import time

saal1 = TalkRecorder(1, "/tmp/")

while True:
  saal1.poll()
  for i in range(60):
    saal1.pollSecond()
    time.sleep(1)
