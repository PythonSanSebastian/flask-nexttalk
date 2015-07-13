import os
import json
from datetime import datetime, timedelta


talks_path = "%s%s" % (os.path.dirname(os.path.abspath(__file__)), "/static/data/talks.json")


class Talks(object):

    raw_talks = None
    time_based_talks = {}

    def __init__(self):
        self.raw_talks = json.loads(open(talks_path, "r").read())
        self.build_time_based_dict()

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

    def filter_talks(self, time_obj):
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
