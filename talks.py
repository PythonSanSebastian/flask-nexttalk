__author__ = 'oier'


import config as cf
import sqlite3


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

# Run
if __name__ == '__main__':
    testing(1)