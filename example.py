#!/usr/bin/python3
from c3recorder import TalkRecorder
import time

saal1 = TalkRecorder('saal1', "/var/www/32c3.ex23.de/saal1/")

while True:
  saal1.poll()
  for i in range(60):
    saal1.pollSecond()
    time.sleep(1)
