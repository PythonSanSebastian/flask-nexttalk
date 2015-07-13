__author__ = 'oier'

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from momentjs import momentjs
import datetime as dt
import pytz
import config as cf
from threading import Thread, Event
from time import sleep
import talks
# Initialize the Flask application
app = Flask(__name__, static_path = '/static', static_url_path = '/static')
app.config['DEBUG'] = True
#app.config['HOST'] = "0.0.0.0"
#app.config['PORT'] = '8080'

#socket = SocketIO(app)

# Set jinja template global
app.jinja_env.globals['momentjs'] = momentjs

@app.route('/Google')
def index():
    my_track = ['Google Room']
    pytz.timezone ("Europe/Madrid")
    naive = dt.datetime.now().replace(minute = 50)
    gtalks = talks.next_session("Google Room",  dt.datetime(2015,7,21,9,30), 3)

    other_talks = []
    actual = dict()
    for r in cf.room_names:
        if r not in my_track:
            t = talks.next_session(r,  dt.datetime(2015,7,21,9,30), 1)
            if t != None:
                actual["track_title"] = r
                actual["time"] = t["start_time"]
                actual["talk"] = t["title"]
                actual["speaker"] = t["speaker"]
                other_talks.append(actual)

    print(dt.datetime.now().replace(minute = 0))
    return render_template('index.html', timestamp=naive, next_talk=gtalks[0], talks=gtalks[1:3], track=other_talks)


# Run
if __name__ == '__main__':
    app.run(
        debug=True,
        host = "0.0.0.0",
        port = 8080
    )