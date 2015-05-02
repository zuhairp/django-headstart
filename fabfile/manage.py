"""
Runs Django manage.py commands on a remote host
Not to be confused with the actual manage.py


"""
import sys

from fabric.api import *
from fabtools import require
import fabtools

import utils

from django.core.management import get_commands

def get_wrapper(command_name):
    def wrapper():
        with cd(utils.get_project_dir()), fabtools.python.virtualenv(utils.get_venv_dir()):
            run('./manage.py %s' % command_name)
    return wrapper

module = sys.modules[__name__]
for command_name in get_commands():
    setattr(module, command_name, task(name=command_name)(get_wrapper(command_name)))






        
