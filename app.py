__author__ = 'oier'

import pytz
from datetime import datetime
from threading import Thread, Event
from time import sleep

from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from momentjs import momentjs

from talks import Talks


# Initialize the Flask application
app = Flask(__name__, static_path='/static', static_url_path='/static')
app.config['DEBUG'] = True

socket = SocketIO(app)
# Set jinja template global
app.jinja_env.globals['momentjs'] = momentjs

thread = Thread()
thread_stop_event = Event()


@app.route('/')
def index():
    pytz.timezone("Europe/Madrid")
    naive = datetime.now().replace(minute=50)

    talks = Talks()
    #current, next_t = talks.filter_talks_by_time(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))
    #print current
    #print next_t

    rooms = talks.filter_talks_by_room(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))

    cur = talks.get_current(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))
    import pprint
    #pprint.pprint(rooms)
    pprint.pprint(cur)
    # Render template with a test timestamp
    print(datetime.now().replace(minute=0))
    return render_template('multi_index.html',
                           timestamp=naive,
                           talks_list=rooms)

@app.route('/menu/')
def menu():
    talks = Talks()
    rooms = talks.filter_talks_by_room(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))
    return render_template('menu.html',
                           options = rooms.keys() )


@app.route('/room/<track>')
def room_info(track):
    return render_room(track)


def render_room(room):
    pytz.timezone("Europe/Madrid")
    naive = datetime.now().replace(minute=50)

    talks = Talks()

    rooms = talks.filter_talks_by_room(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))

    actual = rooms.pop(room)
    other = rooms


    print(datetime.now().replace(minute=0))
    return render_template('index.html',
                           room_name = room,
                           timestamp=naive,
                           next_talk=actual["current"],
                           talks=actual["next"],
                           talks_list=other)


# Run
if __name__ == '__main__':
    # app.run(
    #    debug=True,
    #     host = "0.0.0.0",
    #     port = 80
    # )
    socket.run(app)
