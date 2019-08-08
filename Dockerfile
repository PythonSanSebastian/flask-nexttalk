FROM debian:buster

WORKDIR /opt

ADD . flask_nexttalk

RUN apt update \
    && apt -y upgrade \
    && apt -y install build-essential python3-dev python3-pip \
    && python3 -m pip install -U pip setuptools pipenv \
    && touch /tmp/mysite.sock \
    && chown www-data /tmp/mysite.sock \
    && cd flask_nexttalk/; pipenv install \
    && rm -rf /var/lib/apt/lists/* \


RUN ln -s /etc/uwsgi/apps-available/mysite.ini /etc/uwsgi/apps-enabled/mysite.ini \
    && service nginx restart \
    && service uwsgi restart

# command: /bin/bash -c "envsubst < /etc/nginx/conf.d/mysite.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"

EXPOSE 80


# Now all we have to do is  add our configuration files for nginx and uwsgi. First delete the default configuration for nginx:
# ```
# cd /etc/nginx/sites-available
# sudo rm default
# ```
# Create a new configuration file mysite and add the following:

# ```
# server {
#     listen 80;
#     server_tokens off;
#     server_name localhost;

#      location / {
#          include uwsgi_params;
#          uwsgi_pass unix:/tmp/mysite.sock;
#      }

#      location /static {
#          alias /home/pi/App/flask-nexttalk/ep2017/static;
#      }

#      ## Only requests to our Host are allowed
#      if ($host !~ ^(localhost)$ ) {
#         return 444;
#      }
# }
# ```
# NOTE: change ep2017 for your theme folder

# In order to enable the site, we must link our configuration file to /etc/nginx/sites-enabled/:

# ```
# sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite
# ```


