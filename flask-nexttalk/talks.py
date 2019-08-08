import os
import json
from datetime import datetime, timedelta

import config as cfg


talks_path = cfg.TALKS_PATH

class Talks(object):

    raw_talks = None
    time_based_talks = {}
    room_based_talks = {}

    def __init__(self):
        self.raw_talks = json.loads(open(talks_path, "r").read())
        if not self.time_based_talks:
            self.build_time_based_dict()
        if not self.room_based_talks:
            self.build_room_based_dict()

    def build_time_based_dict(self):
        for key, value in self.raw_talks.items():
            for k, v in value.items():
                # apparently there are some unset timerange keys
                time_range = v.get('timerange') or None
                if time_range is not None:
                    exists = self.time_based_talks.get(time_range)
                    if exists is None:
                        self.time_based_talks[time_range] = []
                    v.update({'talk_type': key})
                    self.time_based_talks[time_range].append(v)

    def build_room_based_dict(self):
        for key, value in self.raw_talks.items():
            for k, v in value.items():
                room = v.get('track_title') or None
                if room:
                    exists = self.room_based_talks.get(room)
                    if exists is None:
                        self.room_based_talks[room] = []
                        v.update({'talk_type': key})
                    self.room_based_talks[room].append(v)

    def filter_talks_by_time(self, time_obj):
        items = self.time_based_talks.keys()
        current_talks = []
        next_talks = []

        for item in items:
            start, end = item.split(",")
            talk_start = datetime.strptime(start.strip(), '%Y-%m-%d %H:%M:%S')
            talk_end = datetime.strptime(end.strip(), '%Y-%m-%d %H:%M:%S')
            next_timeframe = talk_end + timedelta(hours=1.5)

            if talk_start <= time_obj <= talk_end:
                current_talks.extend([i for i in self.time_based_talks[item]])

            if talk_end <= time_obj <= next_timeframe:
                next_talks.extend([i for i in self.time_based_talks[item]])

        return current_talks, next_talks

    def filter_talks_by_room(self, time_obj: datetime):
        talks = {}

        for key, value in self.room_based_talks.items():
            room = talks.get(key)
            if room is None:
                talks[key] = {}
                talks[key]['current'] = []
                talks[key]['next'] = []

            for v in value:
                time_range = v.get('timerange')
                if time_range:
                    timeranges = v.get('timerange').split(",")
                    if len(timeranges) > 2:
                        start, end = timeranges[0], timeranges[-1]
                    else:
                        start, end = timeranges
                    talk_start = datetime.strptime(start.strip(), '%Y-%m-%d %H:%M:%S')
                    talk_end = datetime.strptime(end.strip(), '%Y-%m-%d %H:%M:%S')
                    v['start_hour'] = talk_start.strftime("%H:%M")
                    v['start'] = talk_start
                    v['end'] = talk_end
                    next_timeframe = talk_end + timedelta(hours=1.5)

                    if talk_start <= time_obj <= talk_end:
                        talks[key]['current'].append(v)
                        continue

                    if talk_end <= time_obj <= next_timeframe:
                        talks[key]['next'].append(v)

        return talks


    def get_current_talk(self, time_obj: datetime):
        cur = []
        for key, talk in self.filter_talks_by_room(time_obj).items():
            if talk['current']:
                cur.append(talk['current'])
        return cur

    def get_one_room(self, room, time_obj):
        return self.filter_talks_by_room(time_obj)[room]
