# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime

from invoke import task
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer

CONFIG = {
    # Local path configuration (can be absolute or relative to tasks.py)
    'deploy_path': 'output',
    # Remote server configuration
    'production': 'root@localhost:22',
    'dest_path': '/var/www',
    # Github Pages configuration
    'github_pages_branch': 'gh-pages',
    'commit_message': "'Publish site on {}'".format(datetime.date.today().isoformat()),
    # Port for `serve`
    'port': 8000,
}

@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])

@task
def build(c):
    """Build local version of site"""
    c.run('pelican -s pelicanconf.py')

@task
def rebuild(c):
    """`build` with the delete switch"""
    c.run('pelican -d -s pelicanconf.py')

@task
def serve(c):
    """Serve site at http://localhost:8000/"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG['deploy_path'],
        ('', CONFIG['port']),
        ComplexHTTPRequestHandler,
    )

    sys.stderr.write('Serving on port {port} ...\n'.format(**CONFIG))
    server.serve_forever()

@task
def auto_app(c):
    import subprocess


    commands = [
        "fuser -k 5000/tcp", #kill process in port 5000
        "pip install virtualenv",
        "virtualenv env -p /usr/bin/python2.7",
        "env/bin/pip install -r requirements/dev_requirements.txt",
        "env/bin/python app.py"

    ]

    #run_app = "env/bin/python app.py"

    for i in commands:
        print(i)
        process = subprocess.Popen(i.split(), stdout=subprocess.PIPE)
        process.wait()

    #process = subprocess.Popen(run_app.split(), stdout=subprocess.PIPE)

    #import git

    #g = git.cmd.Git(".")
    #while T:
    #    print(git.pull())


@task
def auto_rpi(c):
    import subprocess


    commands = [
        "fuser -k 5000/tcp", #kill process in port 5000
        "pip install virtualenv",
        "virtualenv env -p /usr/bin/python2.7",
        "env/bin/pip install -r requirements/dev_requirements.txt",
        "env/bin/python app.py",
        "@xset s noblank",
        "@xset s off",
        "@xset -dpms",
        "iceweasel http://0.0.0.0:5000 &",
        "sleep 60",
        "xdotool search --onlyvisible --name iceweasel key F11"
    ]

    #run_app = "env/bin/python app.py"

    for i in commands:
        print(i)
        process = subprocess.Popen(i.split(), stdout=subprocess.PIPE)
        process.wait()

    #process = subprocess.Popen(run_app.split(), stdout=subprocess.PIPE)

    #import git

    #g = git.cmd.Git(".")
    #while T:
    #    print(git.pull())
