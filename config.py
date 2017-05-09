__author__ = 'oier'

import os

DATA_PATH = "data"
DB_NAME = "p3_june_29.db"
DB_PATH = os.path.join(DATA_PATH, DB_NAME)
THEME = "ep2017"

#REMEMBER TO SER THE ROUTES IN APP.PY!!!!!!!
STATIC_PATH = os.path.join(THEME, "static")
TEMPLATES_PATH = os.path.join(THEME, "templates")

TALKS_PATH = "%s%s%s%s" % (os.path.dirname(os.path.abspath(__file__)),"/",THEME, "/static/data/accepted_talks.json")
