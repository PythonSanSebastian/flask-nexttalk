# flask-nexttalk
- Working in python2
- Testing in python3 (fails gevent-socketio)

Instructions:
------
```
pip install -r requirements/dev_requirements.txt
```
```
python app.py
```

Lazy mode:
------

```
python auto_app.py
```

THEMES:
-------

Add THEMES:
1. Create a folder inside /theme
  - Must contain "static" and "templates" folder.
2. select the theme at config.py
```
THEME="ep2017"
```
3. check serve_static function in app.py has all needed app.route definitions

SPONSORS
------

From ep2018 theme sponsors are added automatically if there are in the proper static folder. Folder can be changed in the config.py.

```
#DEFAULT VALUE
SPONSOR_IMAGES = "media/sponsors"
```

SOCIAL PART
-----
Social part is a IFRAME, should be hosted and created somewhere. Last year the social part was created and hosted by  @patrick91 

Source of the Iframe can be easily changed in the config.py file:

```
#There is no "working" default value.
SOCIAL_IFRAME_SRC = "http://your_url.com"
```



SETUP
------
[Follow this tutorial](https://github.com/PythonSanSebastian/flask-nexttalk/blob/ep2016/SETUP.md)

TODO
------
- Automatically sync static/data/talks.json with internet
