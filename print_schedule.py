#!/usr/bin/python3

from c3recorder import ScheduleInterpreter
from jinja2 import Environment, FileSystemLoader
import glob
import os
import datetime, time
import re

def renderTemplate(templateVars, output='fahrplan'):
# Capture our current directory
  THIS_DIR = os.path.dirname(os.path.abspath(__file__))
  j2_env = Environment(loader=FileSystemLoader(THIS_DIR), 
                       trim_blocks=True,
                       extensions=["jinja2.ext.do",])
  outputHtml = j2_env.get_template('fahrplan_template.html').render(templateVars)

  outputHtml = re.sub(' +',' ',outputHtml)

  f = open('/srv/www/html/32c3.ex23.de/{0}.html'.format(output), 'w')
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
t['title'] = "32C3 Fahrplan"
t['talks'] = s.roomlist
t['rooms'] = ['hall1', 'hall2', 'hallg', 'hall6']
t['talkDetailUrl'] = "http://events.ccc.de/congress/2015/Fahrplan/events/{0}.html"
t['currentTime'] = roundTimeTo5Minutes(datetime.datetime.now())

allTalks = []
for k in s.roomlist.keys():
  allTalks.extend(s.roomlist[k])

destDir='/srv/www/html/32c3.ex23.de/'
allRecordingFiles = glob.glob(destDir + '/*/*.webm')
allRecordingFiles.extend(glob.glob(destDir + "/CCC/32C3/*/*.webm"))

for talk in allTalks:
  i=0
  for rec in allRecordingFiles:
    url = rec.split(destDir)[-1]
    if "-"+str(talk.id)+"-" in rec:
      if "_concat_"  in rec:
        talk.urls['complete'] = url
        talk.filesizes['complete'] = os.path.getsize(rec)
      else:
        talk.urls[i] = url
        talk.filesizes[i] = os.path.getsize(rec)
        i+=1
    elif "-"+str(talk.id)+"-" in rec and "CCC/32C3" in rec and ('-hq' in rec or '-hd' in rec):
      talk.urls['OFFICIAL'] = url
      talk.filesizes['OFFICIAL']  = os.path.getsize(rec)

t['timeIntervals'] = getTimeIntervals(getDatetime('2015-12-27 10:00'), getDatetime('2015-12-28 06:00'))
renderTemplate(t, 'fahrplan_d1')
t['timeIntervals'] = getTimeIntervals(getDatetime('2015-12-28 10:00'), getDatetime('2015-12-29 06:00'))
renderTemplate(t, 'fahrplan_d2')
t['timeIntervals'] = getTimeIntervals(getDatetime('2015-12-29 10:00'), getDatetime('2015-12-30 06:00'))
renderTemplate(t, 'fahrplan_d3')
t['timeIntervals'] = getTimeIntervals(getDatetime('2015-12-30 10:00'), getDatetime('2015-12-31 06:00'))
renderTemplate(t, 'fahrplan_d4')

