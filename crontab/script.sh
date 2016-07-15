#!/bin/bash

#CRON TAB FOR AUTO GIT PULL

# instructions:
# sudo apt-get install cron
# crontab -e

# to list contabs:
# crontab -l

# crontab should look liks:
# 59 * * * * sh /home/pi/script.sh

cd ~/App/flask-nexttalk
git pull


