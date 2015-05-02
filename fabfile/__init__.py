from fabric.api import task

from hosts import *
from provisioning import provision
from deployment import *

import manage
import project

provision = task(name="provision")(provision)
runserver = task(name="runserver")(runserver)
gunicorn  = task(name="gunicorn")(gunicorn)
stop      = task(name="stop")(stop)
deploy    = task(name="deploy")(deploy)

# This was spamming the list of commands, now it's gone 4ever... muahahahha
del(provisioning.fabtools.vagrant.vagrant)
