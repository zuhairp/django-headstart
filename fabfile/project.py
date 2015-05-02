"""
Useful commands 

"""

import json

from fabric.api import *

@task
def create_project(name):
    local('django-admin startproject %s .' % name)
    with open('servers.config.json', 'r+') as json_config:
        config = json.load(json_config)
        config['config'] = config.get('config', {})
        config['config']['project_name'] = name
        json_config.seek(0)
        json.dump(config, json_config, indent=4)

