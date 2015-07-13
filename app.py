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
    current, next_t = talks.filter_talks(datetime.strptime('2015-07-22 15:45:00', '%Y-%m-%d %H:%M:%S'))
    print current
    print next_t
    # Render template with a test timestamp
    print(datetime.now().replace(minute=0))
    return render_template('index.html', timestamp=naive, next_talk="next", talks=["talks1", "talks2"])


@socket.on('connect', namespace='/clock')
def clock():
    global thread
    print("Client Connected")

    if not thread.isAlive():
        thread = ClockThread()
        thread.start()


class ClockThread(Thread):
    def __init__(self):
        self.delay = 1
        super(ClockThread, self).__init__()

    def actual(self):
        """
        :return: actual timestamp
        """
        pytz.timezone("Europe/Madrid")
        while not thread_stop_event.isSet():
            naive = datetime.now()
            print(naive)
            socket.emit('newtime', {'time': naive}, namespace='/clock')
            sleep(self.delay)

    def run(self):
        self.actual()


@socket.on('connect', namespace='/clock')
def clock_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print ("Starting Thread")
        thread = ClockThread()
        thread.start()


@socket.on('disconnect', namespace='/clock')
def clock_disconnect():
    print('Client disconnected')

# Run
if __name__ == '__main__':
    # app.run(
    #    debug=True,
    #     host = "0.0.0.0",
    #     port = 80
    # )
    socket.run(app)
