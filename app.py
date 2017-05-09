__author__ = 'oier'

import pytz
from datetime import datetime
from threading import Thread, Event
from time import sleep

from flask import Flask, render_template
from flask import send_from_directory, request
#from flask.ext.socketio import SocketIO
from momentjs import momentjs

from talks import Talks
import config as cfg

import os

# Initialize the Flask application
print(cfg.TEMPLATES_PATH)
app = Flask(__name__, static_path="/" + cfg.STATIC_PATH, static_url_path="/" + cfg.STATIC_PATH, template_folder=cfg.TEMPLATES_PATH)
app.config['DEBUG'] = True

#socket = SocketIO(app)
# Set jinja template global
app.jinja_env.globals['momentjs'] = momentjs

thread = Thread()
thread_stop_event = Event()

#ADD ONE ROUTE PER FOLDER IN STATIC FOLDER
@app.route('/'+ cfg.STATIC_PATH +'/media/fonts/<filename>')
@app.route('/'+ cfg.STATIC_PATH +'/<filename>')
@app.route('/'+ cfg.STATIC_PATH +'/media/sponsors/<path:filename>')
@app.route('/'+ cfg.STATIC_PATH +'/media/<path:filename>')
def serve_sponsors(filename):
    url = os.path.dirname(str(request.url_rule))[1:]
    #root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(url, filename)

@app.route('/')
def index():
    pytz.timezone("Europe/Madrid")
    naive = datetime.now().replace(minute=50)

    talks = Talks()
    #current, next_t = talks.filter_talks_by_time(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))
    #print current
    #print next_t

    #rooms = talks.filter_talks_by_room(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))

    rooms = talks.filter_talks_by_room(datetime.now())

    empty = all([len(rooms[key]['current']) == 0 for key in rooms.keys()])

    cur = talks.get_current(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))
    # import pprint
    # #pprint.pprint(rooms)
    # pprint.pprint(cur)
    # Render template with a test timestamp
    # print(datetime.now().replace(minute=0))
    return render_template('multi_index.html',
                           timestamp=naive,
                           empty=empty,
                           talks_list=rooms)

@app.route('/feeds')
def feeds():
    return render_template('feeds.html',
                           event='europython2016',
                           feed_url='http://www.smartfeedz.com/',
                           static_url="http://www.smartfeedz.com/static/",
                           feed_source='http://www.smartfeedz.com/livepage/live-lite/europython2016/')

@app.route('/menu/')
def menu():
    talks = Talks()
    #rooms = talks.filter_talks_by_room(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))
    rooms = talks.filter_talks_by_room(datetime.now())

    return render_template('menu.html',
                           options = rooms.keys() )


@app.route('/room/<track>')
def room_info(track):
    if "Hall" in track:
        return render_hall(track)
    return render_room(track)

@app.route('/hall')
def render_hall():
    pytz.timezone("Europe/Madrid")
    naive = datetime.now().replace(minute=50)

    talks = Talks()

    #rooms = talks.filter_talks_by_room(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))

    rooms = talks.filter_talks_by_room(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print(rooms.keys())
    actual = rooms.pop("Exhibition Hall / Helpdesk ")

    other = random_talks(rooms)

    print(datetime.now().replace(minute=0))
    return render_template('hall.html',
                           now_happening=actual["current"],
                           will_happen=actual["next"],
                           talks_list=other)

def random_talks(talks):
    ts = []
    for k in talks.keys():
        actual = talks.pop(k)
        ts.append(actual["current"])
        ts.append(actual["next"])
    import random
    return random.sample(ts, 10)


def render_room(room):
    pytz.timezone("Europe/Madrid")
    naive = datetime.now().replace(minute=50)

    talks = Talks()

    #rooms = talks.filter_talks_by_room(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))
    rooms = talks.filter_talks_by_room(datetime.now())

    actual = rooms.pop(room)
    other = rooms

    #next_talks = sorted(actual["next"], key=getattr('start'))
    print(datetime.now().replace(minute=0))
    return render_template('index.html',
                           room_name = room,
                           timestamp=naive,
                           next_talk=actual["current"],
                           talks= actual["next"],
                           talks_list=other)


# Run
if __name__ == '__main__':
    app.run(
       # debug=True,
        host = "0.0.0.0",
        port = 5000
    )
    # socket.run(app)
