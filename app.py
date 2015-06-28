__author__ = 'oier'

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from momentjs import momentjs
from datetime import datetime
import pytz

# Initialize the Flask application
app = Flask(__name__, static_path = '/static', static_url_path = '/static')

# Set jinja template global
app.jinja_env.globals['momentjs'] = momentjs

@app.route('/')
def index():
    pytz.timezone ("Europe/Madrid")
    naive = datetime.now().replace(minute = 50)
    # Render template with a test timestamp
    print(datetime.now().replace(minute = 0))
    return render_template('index.html', timestamp=naive, next_talk="next", talks=["talks1", "talks2"])

@socketio.on('connect', namespace='/clock')
def clock():
    global thread
    print("Client Connected")

    if not thread.isAlive():
        thread = ClockThread()
        thread.start()
# Run
if __name__ == '__main__':
    app.run(
        debug=True,
        #host = "0.0.0.0",
        #port = 80
    )