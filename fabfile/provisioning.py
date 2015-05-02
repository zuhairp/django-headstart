"""
Provisions (i.e. sets up) a server with required dependencies

"""

from fabric.api import *
from fabtools import require
import fabtools

import utils


def provision():
    """
    Provisions the server with PostgreSQL and an Nginx reverse proxy
    Currently only supports Debian (e.g. Ubuntu) targets

    """
    require.deb.packages([
        'libpq-dev',
        'python-dev',
        'postgresql',
        'postgresql-contrib'
    ])

    # Set up a PostgreSQL server with a default user
    require.postgres.server()
    require.postgres.user(
        name=env.user, 
        password=env.password,
        superuser=True
    )
    require.postgres.database(
        name='%(user)s_db' % env,
        owner=env.user
    )

    #Set up Nginix proxied site
    require.nginx.server()
    require.nginx.proxied_site('_', #empty server name
        port=80,
        proxy_url='http://127.0.0.1:8080',
        docroot='%s/www' % utils.get_project_dir(),
    )
    require.nginx.disabled('default')
    require.python.virtualenv('virtual_environment')
