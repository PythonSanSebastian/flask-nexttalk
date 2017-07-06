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
