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


SETUP
------
[Follow this tutorial](https://github.com/PythonSanSebastian/flask-nexttalk/blob/ep2016/SETUP.md)

TODO
------
- Automatically sync static/data/talks.json with internet
