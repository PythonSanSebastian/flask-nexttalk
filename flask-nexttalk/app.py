import os
import logging
from datetime import datetime
from threading import Thread, Event
from time import sleep

import pytz
from flask import Flask, render_template
from flask import send_from_directory, request

from .momentjs import MomentJS
from .talks import Talks
from .sponsors import Sponsors
from .config import (
    LOG_LEVEL,
    STATIC_PATH,
    TEMPLATES_PATH,
    SPONSORS_IMAGES_PATH,
    SOCIAL_IFRAME_SRC,
)


logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


#ADD ONE ROUTE PER FOLDER IN STATIC FOLDER
@app.route('/'+ STATIC_PATH +'/media/fonts/<filename>')
@app.route('/'+ STATIC_PATH +'/<filename>')
@app.route('/'+ STATIC_PATH +'/media/sponsors/<path:filename>')
@app.route('/'+ STATIC_PATH +'/media/<path:filename>')
def serve_static(filename):
    url = os.path.dirname(str(request.url_rule))[1:]
    #root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(url, filename)


@app.route('/')
def index():
    pytz.timezone(LOCAL_TZ)
    naive = datetime.now().replace(minute=50)
    talks = Talks()
    rooms = talks.filter_talks_by_room(datetime.now())
    empty = all([len(rooms[key]['current']) == 0 for key in rooms.keys()])

    sponsors = Sponsors()
    sponsors_list = sponsors.sponsors_list()
    logger.debug(f'Sponsors: {sponsors_list}.')
    return render_template(
        'multi_index.html',
        timestamp=naive,
        empty=empty,
        talks_list=rooms,
        sponsors=sponsors_list,
        social_iframe_src=SOCIAL_IFRAME_SRC,
    )


@app.route('/feeds')
def feeds():
    feeds_link = []
    feeds_link += ['<a class="twitter-grid" data-dnt="true" href="https://twitter.com/search?q=%euroscipy%2C%20OR%20%23ep2017" data-widget-id="861970559399325696">']
    feeds_link += ['Tweets about #euroscipy']
    feeds_link += ['</a>']
    feeds_link += ['<script>']
    feeds_link += ["!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+\"://platform.twitter.com/widgets.js\";fjs.parentNode.insertBefore(js,fjs);}}(document,\"script\",\"twitter-wjs\");"]
    feeds_link += ['</script>']
    return '\n'.join(feeds_link)


@app.route('/menu/')
def menu():
    talks = Talks()
    rooms = talks.filter_talks_by_room(datetime.now())
    return render_template('menu.html', options=list(rooms.keys()),)


@app.route('/room/<track>')
def room_info(track):
    if "Hall" in track:
        return render_hall(track)
    return render_room(track)


@app.route('/hall')
def render_hall():
    pytz.timezone("Europe/Madrid")
    timestamp = datetime.now().replace(minute=50)
    talks = Talks()
    rooms = talks.filter_talks_by_room(timestamp)

    print(rooms.keys())
    actual = rooms.pop("Exhibition Hall / Helpdesk ")

    other = random_talks(rooms)

    print(datetime.now().replace(minute=0))
    return render_template(
        'hall.html',
        now_happening=actual["current"],
        will_happen=actual["next"],
        talks_list=other,
    )


def random_talks(talks):
    ts = []
    for k in talks.keys():
        actual = talks.pop(k)
        ts.append(actual["current"])
        ts.append(actual["next"])
    import random
    return random.sample(ts, 10)


def render_room(room):
    pytz.timezone(cg.LOCAL_TZ)
    naive = datetime.now().replace(minute=50)

    talks = Talks()
    rooms = talks.filter_talks_by_room(datetime.now())
    actual = rooms.pop(room)
    other = rooms

    #next_talks = sorted(actual["next"], key=getattr('start'))
    print(datetime.now().replace(minute=0))
    return render_template(
        'index.html',
        room_name = room,
        timestamp=naive,
        next_talk=actual["current"],
        talks= actual["next"],
        talks_list=other,
    )


def run():
    # Initialize the Flask application
    print(cfg.TEMPLATES_PATH)
    app = Flask(
        __name__,
        static_path="/" + cfg.STATIC_PATH,
        static_url_path="/" + cfg.STATIC_PATH,
        template_folder=cfg.TEMPLATES_PATH
    )
    app.config['DEBUG'] = True

    #socket = SocketIO(app)
    # Set jinja template global
    app.jinja_env.globals['momentjs'] = MomentJS

    thread = Thread()
    thread_stop_event = Event()

    app.run(
       # debug=True,
        host = "0.0.0.0",
        port = 5000
    )
    # socket.run(app)


# Run
if __name__ == '__main__':
    run()
