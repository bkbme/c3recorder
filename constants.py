congressName='34C3'
congressYear='2017'
videoDestDir = '/srv/www/html/{}.ex23.de/'.format(congressName)
scheduleOutputLocation= videoDestDir + '/{0}.html'
scheduleTitle='{} Fahrplan'.format(congressName)
fahrplanHost = "fahrplan.events.ccc.de"
fahrplanUrl = "/congress/{}/Fahrplan/schedule.xml".format(congressYear)
serverUrl = 'https://{}.ex23.de'.format(congressName)

talkDetailUrl = "https://fahrplan.events.ccc.de/congress/2017/Fahrplan/events/{0}.html"
recordingsSearchGlobs = ['/*/*.webm', '/official/*.mp4']
streamurls={ \
            'hallAdams': 'http://cdn.c3voc.de/s1_native_hd.webm', \
            'hallBorg': 'http://cdn.c3voc.de/s2_native_hd.webm', \
            'hallClarke': 'http://cdn.c3voc.de/s3_native_hd.webm', \
            'hallDijkstra': 'http://cdn.c3voc.de/s4_native_hd.webm', \
           }

"""Mapping of room names.
 from external Names (as in the Fahrplan) to linux file friendly names.
 Talk objects use the right side of the table as room names.
"""
rooms = ['hallAdams', 'hallBorg', 'hallClarke', 'hallDijkstra']
roomlist={'Saal Adams': rooms[0], \
          'Saal Borg': rooms[1], \
          'Saal Clarke': rooms[2], \
          'Saal Dijkstra': rooms[3], \
        }

day1 = ['2017-12-27 10:00', '2017-12-28 03:00']
day2 = ['2017-12-28 10:00', '2017-12-29 03:00']
day3 = ['2017-12-29 10:00', '2017-12-30 03:00']
day4 = ['2017-12-30 10:00', '2017-12-31 03:00']
