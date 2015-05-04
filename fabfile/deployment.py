"""
Commands for getting your site up and running!

"""

from fabric.api import *
from fabtools import require
import fabtools

import utils


def migrate():
    """
    Run your migrations, equivalent to fab <target> manage.migrate

    """
    with cd(utils.get_project_dir()), fabtools.python.virtualenv(utils.get_venv_dir()):
        fabtools.python.install_requirements('requirements/requirements-prod.txt')
        run('./manage.py migrate')

def runserver():
    """
    Runs Django's builtin runserver

    """
    with cd(utils.get_project_dir()), fabtools.python.virtualenv(utils.get_venv_dir()):
        fabtools.python.install_requirements('requirements/requirements-prod.txt')
        stop()
        require.supervisor.process('django_app',
            command='%(venv)s/bin/python %(project)s/manage.py runserver 8080' % {'venv': utils.get_venv_dir(), 'project': utils.get_project_dir()},
            user=env.user,
            stopasgroup=True, # manage.py doesn't clean up its children procesess
        )

def gunicorn():
    """
    Runs gunicorn with supervisord. Does not really monitor changes

    """
    with cd(utils.get_project_dir()), fabtools.python.virtualenv(utils.get_venv_dir()):
        fabtools.python.install_requirements('requirements/requirements-prod.txt')
        stop()
        require.supervisor.process('django_app',
            command='%(venv)s/bin/gunicorn -b 127.0.0.1:8080 --chdir %(project_dir)s %(project_name)s.wsgi' % {'venv': utils.get_venv_dir(), 'project_dir': utils.get_project_dir(), 'project_name':env.project_name},
            user=env.user,
            stopasgroup=True, # added for symmetry with manage.py runserver
        )

def stop():
    """
    Stops whatever server process is running

    """
    with settings(warn_only=True):
        fabtools.supervisor.stop_process('django_app')


def deploy(server_type="runserver"):
    if not env.is_vagrant_vm:
        require.git.working_copy(
            remote_url = env.git_repo,
            path = env.project_directory,
            branch = env.git_branch,
        )

    migrate()
    gunicorn() if server_type=="gunicorn" else runserver()
