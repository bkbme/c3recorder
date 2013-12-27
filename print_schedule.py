#!/usr/bin/python3

from c3recorder import ScheduleInterpreter
from jinja2 import Environment, FileSystemLoader
import glob
import os
import datetime, time

def renderTemplate(templateVars, output='fahrplan'):
# Capture our current directory
  THIS_DIR = os.path.dirname(os.path.abspath(__file__))
  j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
  outputHtml = j2_env.get_template('fahrplan_template.html').render(templateVars)

  f = open('/srv/video/{0}.html'.format(output), 'w')
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
t['title'] = "30C3 Fahrplan"
t['talks'] = s.roomlist
t['rooms'] = ['saal1', 'saal2', 'saalg', 'saal6']
t['talkDetailUrl'] = "http://events.ccc.de/congress/2013/Fahrplan/events/{0}.html"
t['currentTime'] = roundTimeTo5Minutes(datetime.datetime.now())

allTalks = []
for k in s.roomlist.keys():
  allTalks.extend(s.roomlist[k])

destDir='/srv/video/'
allRecordingFiles = glob.glob(destDir + '/*/*.mp4')

for talk in allTalks:
  i=0
  for rec in allRecordingFiles:
    if "_"+str(talk.id)+"_" in rec:
      url = rec.split(destDir)[-1]
      if "_concat_"  in rec:
        talk.urls['complete'] = url
      else:
        talk.urls[i] = url
        i+=1

t['timeIntervals'] = getTimeIntervals(getDatetime('2013-12-27 10:00'), getDatetime('2013-12-28 06:00'))
renderTemplate(t, 'fahrplan_d1')
t['timeIntervals'] = getTimeIntervals(getDatetime('2013-12-28 10:00'), getDatetime('2013-12-29 06:00'))
renderTemplate(t, 'fahrplan_d2')
t['timeIntervals'] = getTimeIntervals(getDatetime('2013-12-29 10:00'), getDatetime('2013-12-30 06:00'))
renderTemplate(t, 'fahrplan_d3')
t['timeIntervals'] = getTimeIntervals(getDatetime('2013-12-30 10:00'), getDatetime('2013-12-31 06:00'))
renderTemplate(t, 'fahrplan_d4')

