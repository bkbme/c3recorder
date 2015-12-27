#!/usr/bin/python3
from c3recorder import ScheduleInterpreter
from datetime import datetime, timedelta, date, time
import os
import fnmatch

#Constants
serverUrl="http://32c3.ex23.de/"
fahrplanUrl="http://events.ccc.de/congress/2015/Fahrplan/events/"
listOutput="/srv/video/html/DataTables/list.html"
recordingLocation="/srv/video/"

s = ScheduleInterpreter()
s.createTalksLists()

day = [datetime.now()]*5
day[1] = datetime.strptime("2013-12-27", "%Y-%m-%d")
day[2] = datetime.strptime("2013-12-28", "%Y-%m-%d")
day[3] = datetime.strptime("2013-12-29", "%Y-%m-%d")
day[4] = datetime.strptime("2013-12-30", "%Y-%m-%d")

talksByDay = []
talksByDay.append([])
allTalks = []
for k in s.roomlist.keys():
  allTalks.extend(s.roomlist[k])
for i in range(1, 5):
  talksByDay.append([])
  for talk in allTalks:
    if (talk.startDate.date() == day[i].date()):
      talksByDay[i].append(talk)
  talksByDay[i] = sorted(talksByDay[i], key = lambda talk: talk.startDate)


class recording(object):
  def __init__(self, talk):
    self.talk = talk
    self.official = False
  def setFilename(self, filename):
    self.size = os.path.getsize(filename)
    self.filename = filename
    if "official" in filename:
      self.official = True
  def getArray(self):
    rv = ""
    rv = "[ \"<a href=\\\"{8}{0}.html\\\">{0}</a>\"," \
       + "\"{6}{1}{7}\"," \
       + "\"{2}\"," \
       + "\"{3}\"," \
       + "\"{4}\"," \
       + "\"<a href=\\\"{9}/{5}\\\">download</a>\" ]"
    rv = rv.format(str(self.talk.id), \
                  self.talk.title.replace("_", " ") + (" (official)" if self.official else ""),
                  self.talk.room,
                  self.talk.startDate,
                  str(round(self.size/(1024*1024), 2)),
                  self.filename.replace(recordingLocation, ""),
                  "<strong>" if self.official else "",
                  "</strong>" if self.official else "",
                  fahrplanUrl,
                  serverUrl
                  )

    return rv

recordings = []
for talk in allTalks:
  for root, dirnames, filenames in os.walk(recordingLocation):
    for filename in filenames:
      if(str(talk.id)+'_' in filename and
        (filename[-4:] == '.mp4' or filename[-8:] == 'h264.mp4' or filename[-4:] == '.wmv')):
        r = recording(talk)
        r.setFilename(root + '/' + filename)
        recordings.append(r)


frameStart="{ \"aaData\": ["
frameEnd="] }"

content=""
for i in range(0, len(recordings)):
  r = recordings[i]
  content += r.getArray()
  if( i < len(recordings)-1 ):
    content += ","

out = open(listOutput, "w")
out.write(frameStart)
out.write(content)
out.write(frameEnd)
out.close()
