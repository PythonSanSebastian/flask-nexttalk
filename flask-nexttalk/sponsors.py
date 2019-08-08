import os
import json
from datetime import datetime, timedelta

import config as cfg


class Sponsors:

    sponsors = {}

    def __init__(self):
        sponsors_path = cfg.SPONSORS_IMAGES_PATH
        print(sponsors_path)
        sponsor_image_list = os.listdir(sponsors_path)
        for i in sponsor_image_list:
            print(i)
            path = os.path.join(cfg.SPONSORS_IMAGES, i)
            name = os.path.splitext(i)[0]
            print(path)
            print(name)

            self.sponsors[name] = path

    def sponsors_list(self):
        return self.sponsors
