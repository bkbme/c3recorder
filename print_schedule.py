#!/usr/bin/python3

from c3recorder import ScheduleInterpreter
from jinja2 import Environment, FileSystemLoader
import glob
import os
import datetime, time
import re
import collections
import constants

def renderTemplate(templateVars, output='fahrplan'):
# Capture our current directory
  THIS_DIR = os.path.dirname(os.path.abspath(__file__))
  j2_env = Environment(loader=FileSystemLoader(THIS_DIR), 
                       trim_blocks=True,
                       extensions=["jinja2.ext.do",])
  outputHtml = j2_env.get_template('fahrplan_template.html').render(templateVars)

  outputHtml = re.sub(' +',' ',outputHtml)

  f = open(constants.scheduleOutputLocation.format(output), 'w')
  f.write(outputHtml)
  f.close()

def getTimeIntervals(startDate, endDate, gratingMinutes=5):
  delta = datetime.timedelta()
  timeIntervalList = []
  while(startDate + delta < endDate):
    timeIntervalList.append(startDate+delta)
    delta += datetime.timedelta(minutes=gratingMinutes)
  return timeIntervalList

def getDatetime(string):
  return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M")

def roundTimeTo5Minutes(tm):
  tm = tm - datetime.timedelta(minutes=tm.minute %5,
                               seconds=tm.second,
                               microseconds=tm.microsecond)
  return tm

s = ScheduleInterpreter()
s.getSchedule()
s.createTalksLists()

t = dict()
t['title'] = constants.scheduleTitle
t['talks'] = s.roomlist
t['rooms'] = constants.rooms
t['talkDetailUrl'] = constants.talkDetailUrl 
t['currentTime'] = roundTimeTo5Minutes(datetime.datetime.now())

allTalks = []
for k in s.roomlist.keys():
  allTalks.extend(s.roomlist[k])

destDir=constants.videoDestDir
allRecordingFiles = []
for location in constants.recordingsSearchGlobs:
    allRecordingFiles.extend(glob.glob(destDir + location))

for talk in allTalks:
  i=0
  for rec in allRecordingFiles:
    url = rec.split(destDir)[-1]
    if "-"+str(talk.id)+"-" in rec and "official" in url:
      talk.urls['OFFICIAL'] = url
      talk.filesizes['OFFICIAL']  = os.path.getsize(rec)
    elif "-"+str(talk.id)+"-" in rec:
      if "_concat_"  in rec:
        talk.urls['complete'] = url
        talk.filesizes['complete'] = os.path.getsize(rec)
      else:
        talk.urls[i] = url
        talk.filesizes[i] = os.path.getsize(rec)
        i+=1

t['timeIntervals'] = getTimeIntervals(getDatetime(constants.day1[0]), getDatetime(constants.day1[1]))
renderTemplate(t, 'fahrplan_d1')
t['timeIntervals'] = getTimeIntervals(getDatetime(constants.day2[0]), getDatetime(constants.day2[1]))
renderTemplate(t, 'fahrplan_d2')
t['timeIntervals'] = getTimeIntervals(getDatetime(constants.day3[0]), getDatetime(constants.day3[1]))
renderTemplate(t, 'fahrplan_d3')
t['timeIntervals'] = getTimeIntervals(getDatetime(constants.day4[0]), getDatetime(constants.day4[1]))
renderTemplate(t, 'fahrplan_d4')

