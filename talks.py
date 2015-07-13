__author__ = 'oier'


import config as cf
import sqlite3

import json
import datetime as dt
import utils as ut
import config as cf
from   operator import itemgetter


def testing(day=1):
    conn = sqlite3.connect(cf.DB_PATH)
    c = conn.cursor()
    #SCHEDULE ID is about DAY, starting 1 to 7 (conference_schedule)
    '''
    events: id, schedule_id, start_time, talk_id, custom, abstract, duration, tags, sponsor_id, video, streaming, bookable, seats
    eventtracks: idm track_id, event_id
    talk: id, title, slug, duration, conference, duration, qa_duration, language, slides, video_tyoe, ...
    ... level
    takspeaker = talk_id, speaker_name, speaker_last_name
    '''

    events = c.execute("SELECT * FROM conference_event WHERE schedule_id="+str(day)).fetchall()
    event_in_room = c.execute("SELECT" +
                           " conference_eventtrack.event_id," +
                           " conference_track.title" +
                           " FROM conference_eventtrack JOIN conference_track" +
                           " ON conference_eventtrack.track_id=conference_track.id").fetchall()

    talk = c.execute("SELECT id,title,duration,level FROM conference_talk").fetchall()
    talkspeaker = c.execute("SELECT talk_id,first_name,last_name "+
                            "FROM conference_talkspeaker JOIN auth_user "+
                            "ON conference_talkspeaker.speaker_id=auth_user.id").fetchall()


    for e in events:
        print(e[0])

    conn.close()



#################
# GET TALKS FROM JSON
################

def talk_schedule_2(start, end):

    input_format  = "%Y-%m-%d %H:%M:%S"
    output_format_day = "%A, %B"
    output_format_time = "%H:%M"

    output_day = lambda d: "{}".format(d.strftime("%d"))

    output_hour = lambda d: "{}".format(d.strftime(output_format_time))

    start_date = dt.datetime.strptime(start, input_format)
    end_date   = dt.datetime.strptime(end  , input_format)

    return output_day(start_date), output_hour(start_date), output_day(end_date), output_hour(end_date)

def get_all_talks_from_room(room):
    ts = []
    for session_name in cf.session_names:
        talks = cf.talk_sessions[session_name]
        talks = [talks[talk_id] for talk_id in talks]
        talks = sorted(talks, key=itemgetter('title'))
        for talk in talks:
            if (ut.to_str(talk.get('track_title', '').split(', ')[0]) == room):
                speakers  = ut.to_str(talk['speakers'])
                title     = ut.to_str(talk['title'])
                timerange = ut.to_str(talk.get('timerange', '').split(';')[0])
                try:
                    start_date, start_hour, end_day, end_hour = talk_schedule_2(*timerange.split(', '))
                except:
                    start, end = ('', '')

                t = { 'speaker': speakers,
                    'title': title,
                    'start_date': start_date,
                    'start_time': start_hour,
                     'end_date': end_day,
                    'end_time': end_hour}
                ts.append(t)
    return(ts)

def next_session(room, time, quant=1):
    input_format = "%H:%M"
    ts = get_all_talks_from_room(room)
    ts = sorted(ts, key=itemgetter("start_date", "start_time"))
    next_session = []
    for talk in ts:
        if int(talk["start_date"]) == time.day:
            start_dt_hour = dt.datetime.strptime(talk["start_time"], input_format)
            if start_dt_hour.time() > time.time():
                next_session.append(talk)
    return(next_session[0:quant])

# Run
if __name__ == '__main__':
    print(next_session("Google Room", dt.datetime(2015,7,21,9,30),3))