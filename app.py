__author__ = 'oier'

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from momentjs import momentjs
from datetime import datetime
import pytz
from threading import Thread, Event
from time import sleep

# Initialize the Flask application
app = Flask(__name__, static_path = '/static', static_url_path = '/static')
app.config['DEBUG'] = True
#app.config['HOST'] = "0.0.0.0"
#app.config['PORT'] = '8080'

#socket = SocketIO(app)

# Set jinja template global
app.jinja_env.globals['momentjs'] = momentjs

@app.route('/')
def index():
    pytz.timezone ("Europe/Madrid")
    naive = datetime.now().replace(minute = 50)
    # Render template with a test timestamp
    print(datetime.now().replace(minute = 0))
    return render_template('index.html', timestamp=naive, next_talk="next", talks=["talks1", "talks2"])

'''
@socket.on('connect', namespace='/clock')
def clock():
    global thread
    print("Client Connected")

    if not thread.isAlive():
        thread = ClockThread()
        thread.start()


thread = Thread()
thread_stop_event = Event()

'''

'''
class ClockThread(Thread):
    def __init__(self):
        self.delay = 1
        super(ClockThread, self).__init__()

    def actual(self):
        pytz.timezone ("Europe/Madrid")
        while not thread_stop_event.isSet():
            naive = datetime.now()
            print(naive)
            socket.emit('newtime', {'time' : naive}, namespace='/clock')
            sleep(self.delay)

    def run(self):
        self.actual()

'''

'''
@socket.on('connect', namespace='/clock')
def clock_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print ("Starting Thread")
        thread = ClockThread()
        thread.start()

@socket.on('disconnect', namespace='/clock')
def clock_disconnect():
    print('Client disconnected')
'''

# Run
if __name__ == '__main__':
    app.run(
        debug=True,
        host = "0.0.0.0",
        port = 8080
    )
    ##socket.run(app)