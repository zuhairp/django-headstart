"""
Loads the hosts from server.config.json and creates tasks for each of them

Each task sets the environment appropriately

"""

import sys
import json

from fabric.api import *
from fabtools import require
import fabtools
import fabtools.vagrant


def _build_env(server_config, extra_config):
    def host_task():
        print "running on %(pretty_name)s" % server_config

        if server_config["is_vagrant_vm"]:
            config = fabtools.vagrant.ssh_config(server_config["vagrant_name"])
            extra_args = fabtools.vagrant._settings_dict(config)
            env.update(extra_args)

        env.update(server_config)
        env.update(extra_config)

    return host_task

def create_hosts():
    with open("servers.config.json", "r") as config_json:
        server_config = json.load(config_json)
    module = sys.modules[__name__]
    extra_config = server_config.get("config", {})
    for server, config in server_config.items():
        if server == "config": continue
        env_task = _build_env(config, extra_config)
        command = task(name=server)(env_task)
        command.__doc__ = "Run the following task on %(pretty_name)s" % config
        setattr(module, server, command)

        for alias in config['aliases']:
            command = task(name=alias)(env_task)
            command.__doc__ = "Run the following task on %(pretty_name)s" % config
            setattr(module, alias, command)
create_hosts()
