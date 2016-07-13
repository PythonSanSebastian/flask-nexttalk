#!/usr/bin/python3

import json

with open("static/data/talk_abstracts.json") as talks:
    data = json.load(talks)
    for t in data:
        for e in  data[t]:
            del data[t][e]["emails"]

    json.dump(data, open("static/data/clean-talks.json", "w"))


