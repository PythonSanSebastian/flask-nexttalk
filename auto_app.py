import subprocess

commands = [
    "pip install virtualenv",
    "virtualenv env -p /usr/bin/python2.7",
    "env/bin/pip install -r requirements/dev_requirements.txt",
    "env/bin/python app.py"
]


for i in commands:
    print(i)
    process = subprocess.Popen(i.split(), stdout=subprocess.PIPE)
    process.wait()