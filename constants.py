congressName='35c3'
congressYear='2018'
videoDestDir = '/srv/data/muell/{}/'.format(congressName)
scheduleOutputLocation = '/var/www/35c3/' + '/{0}.html'
scheduleTitle='{} Fahrplan'.format(congressName)
fahrplanHost = "fahrplan.events.ccc.de"
fahrplanUrl = "/congress/{}/Fahrplan/schedule.xml".format(congressYear)
serverUrl = 'http://server.home.local/{}'.format(congressName)

talkDetailUrl = "https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/{0}.html"
recordingsSearchGlobs = ['/*/*.webm', '/official/*.mp4']
streamurls={ \
            'hallAdams': 'http://cdn.c3voc.de/s1_native_hd.webm', \
            'hallBorg': 'http://cdn.c3voc.de/s2_native_hd.webm', \
            'hallClarke': 'http://cdn.c3voc.de/s3_native_hd.webm', \
            'hallDijkstra': 'http://cdn.c3voc.de/s4_native_hd.webm', \
            'hallEliza': 'http://cdn.c3voc.de/s5_native_hd.webm', \
           }

"""Mapping of room names.
 from external Names (as in the Fahrplan) to linux file friendly names.
 Talk objects use the right side of the table as room names.
"""
rooms = ['hallAdams', 'hallBorg', 'hallClarke', 'hallDijkstra', 'hallEliza']
roomlist={'Adams': rooms[0], \
          'Borg': rooms[1], \
          'Clarke': rooms[2], \
          'Dijkstra': rooms[3], \
          'Eliza': rooms[4]
        }

day1 = ['2018-12-27 10:00', '2018-12-28 03:00']
day2 = ['2018-12-28 10:00', '2018-12-29 03:00']
day3 = ['2018-12-29 10:00', '2018-12-30 03:00']
day4 = ['2018-12-30 10:00', '2018-12-31 03:00']
