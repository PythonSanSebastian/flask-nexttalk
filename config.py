__author__ = 'oier'

import os
import json

DATA_PATH = "data"

DB_NAME = "p3_june_29.db"

DB_PATH = os.path.join(DATA_PATH,DB_NAME)

talk_sessions = json.load(open('static/data/talks.json'))
talks_admin_url = 'https://ep2015.europython.eu/admin/conference/talk'

session_names = ['Keynotes', 'Talks', 'Trainings', 'Help desks',
                 'EuroPython sessions', 'Other sessions', 'Poster sessions']

room_names = ['Barria2 Room (Education Summit)', 'Barria2 Room', 'Room A4',
              'A2 Room', 'Room B Terrace', 'Room C1', 'Barria1 Room',
              'PythonAnywhere Room', 'Google Room', 'Exhibition Hall / Helpdesk ',
              'Barria2 Room (Local Track)']
