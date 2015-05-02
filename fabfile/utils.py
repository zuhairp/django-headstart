"""
Random useful functions

"""

from fabric.api import *

def get_project_dir():
    if env.is_vagrant_vm:
        return "/vagrant"
    else:
        return env.project_directory

def get_venv_dir():
    if "virtualenv_dir" in env:
        return env.virtualenv_dir
    else:
        return "/home/%(user)s/virtual_environment" % env
