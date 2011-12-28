#!/usr/bin/python3
import xml.etree.ElementTree 
from datetime import datetime, timedelta, date, time

class Talk:
  """Class representing a ccc talk"""
  def __init__(self, title, day, start, duration, room, id, lang):
    """Create instance of Talk class:
    title     -- The title of the talk
    day       -- The day on which the talk is held
    start     -- Starttime when the talk starts (e.g. "11:30")
    duration  -- The duration of the talk (e.g. "01:00" -> 1h)
    room      -- Name of the room the talk is held in
    id        -- Id number of the talk (e.g. 1234)
    lang      -- Language the talk is held on (e.g. "en")
    """
    self.title = title
    self.startDate = datetime.strptime(day + " " + start, "%Y-%m-%d %H:%M")

    """Work around for wired schedule notation: 
    talk starting on 27-12 01:30 is actually starting on
    28-12
    """
    if self.startDate.hour < 11:
      self.startDate += timedelta(days=1)
    duration_time = timedelta(hours=int(duration.split(':')[0]), minutes=int(duration.split(':')[1]));
    if room == "Saal 1":
      self.room = "saal1"
    elif room == "Saal 2":
      self.room = "saal2"
    elif room == "Saal 3":
      self.room = "saal3"

    self.endDate = self.startDate + duration_time
    self.lang = lang
    self.id = id
  def printit(self):
    """Debug helper"""
    print("({}) start({}) end ({}) room({})".format(self.title, self.startDate, self.endDate, self.room))
  def fileName(self):
    """Return filename for the recording"""
    return "28c3-{}-{}-{}-{}-{}".format(self.id, self.lang, self.room, self.startDate.strftime("%Y-%m-%d_%H-%M"), self.title)

class ScheduleInterpreter:
  """This class can download the xml schedule,
  create talk objects from it,
  sort the talks by date and time
  and calculate what is going on right now.
  """
  host = "events.ccc.de"
  url  = "/congress/2011/Fahrplan/schedule.en.xml"
  def getSchedule(self):
    """Get xml schedule from the web and parse the xml.
    Save downloaded xml to file.
    If the downloading of the schedule fails, use the previously 
    downloaded xml file.
    """
    data = None
    import http.client

    try:
      conn = http.client.HTTPConnection(self.host)
      conn.request("GET", self.url)
      r1 = conn.getresponse()
      data = r1.read().decode("utf-8")
    except:
      pass

    """Add a litte redundancy: if parsing of downloaded content fails 
       aka. server is not available, then load the schedule from previously saved file"""
    tree = None
    try:
      tree = xml.etree.ElementTree.fromstring(data)
      schedXml = open("schedule.en.xml", "w")
      schedXml.write(data)
      schedXml.close()
    except: 
      print("Failed to download schedule!")
      schedXml = open("schedule.en.xml", "r")
      data = schedXml.read()
      tree = xml.etree.ElementTree.fromstring(data)
      schedXml.close()
    return tree

  def createTalksLists(self):
    """use getSchedule to download schedule.
    Create members "saal1", "saal2", "saal3", which
    represent a sorted list of talks.
    """
    schedule = self.getSchedule()
    days = schedule.getiterator("day")

    talkList = []
    for day in days:
      events = day.getiterator("event")
      for event in events:
        talk_id = event.attrib["id"]
        talk_slug = event.find("slug").text
        talk_start = event.find("start").text
        talk_duration = event.find("duration").text
        talk_lang = event.find("language").text
        talk_room = event.find("room").text

        if talk_room == None: 
          talk_room = ""
        if talk_lang == None: 
          talk_lang = "en"
        if talk_slug == None:
          talk_slug = ""
        
        theTalk = Talk(talk_slug, day.attrib["date"], \
                       talk_start, talk_duration, talk_room, \
                       talk_id, talk_lang)
        
        talkList.append(theTalk)

    saal1 = []
    saal2 = []
    saal3 = []
    for talk in talkList:
      if talk.room == "saal1":
        saal1.append(talk)
      if talk.room == "saal2":
        saal2.append(talk)
      if talk.room == "saal3":
        saal3.append(talk)

    saal1 = sorted(saal1, key = lambda talk: talk.startDate)
    saal2 = sorted(saal2, key = lambda talk: talk.startDate)
    saal3 = sorted(saal3, key = lambda talk: talk.startDate)
    self.saal1 = saal1
    self.saal2 = saal2
    self.saal3 = saal3

  def getLDND(self, roomNo, now):
    """Get last delta time and next delta time for
    the last, next talk.
    roomNo -- the room you want the info of
    now    -- datetime object representing the current date/time

    returns lastDelta, lastTalk, nextDelta, nextTalk, currentTalk
    """
    if roomNo == 1:
      talksListOfRoom = self.saal1
    elif roomNo == 2:
      talksListOfRoom = self.saal2
    elif roomNo == 3:
      talksListOfRoom = self.saal3

    found = False
    i=0
    t = talksListOfRoom[0]
    #What has just ended?
    while t.endDate < now:
      i += 1
      t = talksListOfRoom[i]

    i -= 1
    t = talksListOfRoom[i]

    endedTalk = t.endDate
    lastTalk = t
    nextTalk = None
    tn = None
    if len(talksListOfRoom) < i+1:
      nextTalk = timedelta(hours=12)
      tn = None
    else:
      tn = talksListOfRoom[i+1]
      nextTalk = tn.startDate # Last talk!?!

    lastDelta = (now - endedTalk).seconds / 60
    nextDelta = (nextTalk - now).seconds / 60
   
    #Get current talk
    ct = None
    for t in talksListOfRoom:
      if t.startDate < now and t.endDate > now:
        ct = t
        break

    return lastDelta, lastTalk, nextDelta, tn, ct


from subprocess import Popen

class FileWriter:
  """Class for recording talks, encapsulating mplayer"""
  streamurl = "http://wmv.28c3.fem-net.de/saal"
  def __init__(self, destination, roomNo):
    """Create an instance of the FileWriter class
    destination -- destination file where the talk should be written to
    roomNo      -- roomNumber which should be recorded
    """
    self.destination = destination
    self.roomNo = roomNo

  def poll(self):
    """Call this periodically to make sure that
    the recording process is still running.
    Should be called about every second.
    """
    if self.process.poll() != None:
      self.start()

  def stop(self):
    """Stop the recording"""
    self.process.terminate()

  def start(self):
    """Start the recording"""
    filename = self.destination + "-" + datetime.now().isoformat() + ".avi"
    print(filename)
    p = Popen(["mplayer", self.streamurl + str(self.roomNo), "-dumpstream", "-dumpfile", filename])
    self.pid = p.pid 
    self.filename = filename
    self.process = p 

class TalkRecorder:
  """Class managing the recording of talks.
  """
  scheduleInterpreter = ScheduleInterpreter()
  def __init__(self, roomNo, recDir):
    """Create an instance of the TalkRecorder class.
    roomNo -- The number of the room this recorder should manage (e.g. 1)
    recDir -- The directory which should contain the recordings
    """
    self.roomNo = roomNo
    self.recDir = recDir
    self.fw = None
    self.refreshSchedCnt = 0
    self.scheduleInterpreter.createTalksLists()

  def pollSecond(self):
    """Call this every second to make sure the recording process is
    still running
    """
    if self.fw != None:
      self.fw.poll()
    
  def poll(self):
    """Call this periodically to check the schedule for
    starting/stopping/restarting the recording.
    Shoud be called every minute.
    """
    now = datetime.now()
    ld, lt, nd, nt, ct = self.scheduleInterpreter.getLDND(self.roomNo, now)
    
    print("-----TalkRecorder for ", self.roomNo, "------")
    if ct != None:
      print("There is a current talk running: ", ct.fileName())
      if self.fw == None:
        self.fw = FileWriter(self.recDir + nt.fileName(), self.roomNo)
        self.fw.start()
    else:
      print("The last talk was", lt.fileName(), " and it was ", ld, "ago")
      print("The next talk is", nt.fileName(), " and it will start in ", nd)
      if abs(nd-ld) < 2:
        print("Good time to restart recording")
        if self.fw != None:
          self.fw.stop()
          self.fw = FileWriter(self.recDir + nt.fileName(), self.roomNo)
          self.fw.start()
      elif nd < 10 and self.fw == None: 
        print("Good time to start recording")
        if self.fw == None:
          self.fw = FileWriter(self.recDir + nt.fileName(), self.roomNo)
          self.fw.start()
      if nd > 60 and ld > 60:
        print("Good time to end recording and call it a day...")
        if self.fw != None:
          self.fw.stop()
          self.fw = None
    if self.refreshSchedCnt > 10:
      r.createTalksLists()
    self.refreshSchedCnt += 1

