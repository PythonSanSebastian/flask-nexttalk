# SETUP
This might not be the best setup, but it is easy to do and it works.
<br>Tested in a rpi3 model b.

## Step 0:

Clone this repository somewhere in you computer/server.

In this tutorial the path will be /home/pi/App/flask-nexttalk

## Step by step:
 based on http://markjberger.com/flask-with-virtualenv-uwsgi-nginx/
 
 We are going to set a nginx server, this will execute our app automaticaly.
 For the nginx server we are going to need 
 
 Intall the basics:
 
 ``` 
 sudo apt-get install build-essential python-dev python-pip
 sudo pip install virtualenv
 ```
 Check that you are the owner of the App. If not:
 
 ```
 sudo chown -R <your user id> /home/pi/App/flask-nexttalk
 ```
 Create a virtual environment (we created inside flask-nexttalk folder, but it is not a requirement)
 
 ```
 cd /home/pi/App/flask-nexttalk
 virtualenv env --no-site-packages
 source .env/bin/activate
 pip install -r requirements/dev_requirements.txt
 ```
 Install nginx:
 
 ```
 sudo apt-get install nginx uwsgi uwsgi-plugin-python
 ```
 Next we must create a socket file for nginx to communicate with uwsgi:
 
 ```
 cd /tmp/
touch mysite.sock
sudo chown www-data mysite.sock
```

Now all we have to do is  add our configuration files for nginx and uwsgi. First delete the default configuration for nginx:
```
cd /etc/nginx/sites-available
sudo rm default
```
Create a new configuration file mysite and add the following:

```
server {
    listen 80;
    server_tokens off;
    server_name localhost;

     location / {
         include uwsgi_params;
         uwsgi_pass unix:/tmp/mysite.sock;
     }

     location /static {
         alias /home/pi/App/flask-nexttalk/ep2017/static;
     }

     ## Only requests to our Host are allowed
     if ($host !~ ^(localhost)$ ) {
        return 444;
     }
}
```
NOTE: change ep2017 for your theme folder

In order to enable the site, we must link our configuration file to /etc/nginx/sites-enabled/:

``` 
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite
```
The process is similar for uwsgi. Create the file /etc/uwsgi/apps-available/mysite.ini and add the following:
```
[uwsgi]
vhost = true
socket = /tmp/mysite.sock
venv = /home/pi/App/flask-nexttalk/env
chdir = /home/pi/App/flask-nexttalk
module = app
callable = app
```
Link the configuration file to the enabled-apps folder:

```
sudo ln -s /etc/uwsgi/apps-available/mysite.ini /etc/uwsgi/apps-enabled/mysite.ini
```

Restart everything
```
sudo service nginx restart
sudo service uwsgi restart
```
If error occurs here check if you forgot an ; in any place. Otherwise it should be working.

Common errors:
* Check that your flask site runs under virtualenv without any errors.
* Ensure that you can run your site with just uwsgi from the command line.
* If you run uwsgi with sudo you will change the owner of mysite.sock to root and this will create errors for nginx. Make sure that you change the owner back to www-data.
* If uwsgi cannot find your app, you probably have an issue with file permissions. In order to serve the site uwsgi must have executable permissions for your python script and your .env folder.
* The logs for nginx and uwsgi are /var/log/nginx/error.log and /var/log/uwsgi/app/mysite.log respectively. If nginx is working properly, you will want to look at /var/log/nginx/access.log.


In this point we need to set a method to load automatically a web navigator and remove cursor and screensaver/blank options.

We did choose iceweasel/firefox as our web client. 

```
sudo apt-get install iceweasel
```

Iceweasel and firefox have a plugin to start in fullscreen mode. <br>
This plugin is rKiosk and you can find it here: https://addons.mozilla.org/en-US/firefox/addon/r-kiosk/ <br>
INSTALL IT!

We are going to use unclutter to remove the cursor.

```
sudo apt-get install unclutter
```
After this we are going to set everything in the autostart file for LXDE.

```
~/.config/lxsession/LXDE-pi/autostart
```

Add this to the file.

```
@unclutter -idle 0
@iceweasel localhost
@xset s noblank 
@xset s off 
@xset -dpms
```

WE ARE DONE!!!! YOUR SERVER SHOULD BE WORKING HERE!!!!

If you want to recover your cursor you can use this command. <br>
Remember: crtl+alt+t opens a terminal

```
unclutter -visible
```




