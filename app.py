__author__ = 'oier'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from itertools import islice, chain
from threading import Thread, Event
from time import sleep
import datetime as dt

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from momentjs import momentjs
import pytz

from converters import RoomsConverter
import config as cf
import talks

# Initialize the Flask application
app = Flask(__name__, static_path='/static', static_url_path='/static')
app.url_map.converters['rooms'] = RoomsConverter
app.config['DEBUG'] = True
#app.config['HOST'] = "0.0.0.0"
#app.config['PORT'] = '8080'

#socket = SocketIO(app)

# Set jinja template global
app.jinja_env.globals['momentjs'] = momentjs


@app.route('/rooms/<rooms:room>')
def index(room):
    pytz.timezone("Europe/Madrid")
    naive = dt.datetime.now().replace(minute=50)
    # Next session returns a generator, we're only interested in N talks,
    # so we use itertools.islice to get those n talks.
    room_talks = islice(talks.next_session(room, dt.datetime(2015, 7, 21, 9, 30)), 3)

    other_rooms = [r for r in cf.room_names if r != room]

    other_talks = []
    for r in other_rooms:
        other_talks = chain(talks.next_session(r,  dt.datetime(2015, 7, 21, 9, 30)), other_talks)

    return render_template('index.html',
                           timestamp=naive,
                           next_talk=next(room_talks),
                           talks=room_talks,
                           track=other_talks)


# Run
if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8080
    )
