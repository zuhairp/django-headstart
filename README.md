# django-headstart

Get a headstart on your Django project. With only a handful of commands, you'll be able to:
* Get a Vagrant VM up and running
* Provision a VM or any SSH-ble server provisioned with all the packages you need. Out of the box, you get a PostgreSQL database and an Nginx reverse proxy
* Develop your app with either Django's built in development server or use Gunicorn as your application server
* Control it all with [Fabric](http://www.fabfile.org/)

### Getting Started

#### Prereqs
Before you begin, you'll need to install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/)

You will also need Python 2.7 installed as well as pip. Virtualenv is highly recommended

#### Getting a headstart
For the purposes of this walkthrough, I'll be calling my project "myapp" (Creative, I know)

(Optional, very highly recommended)
```bash
virtualenv myapp_venv
source myapp_venv/bin/activate
```
Rember to always source the virtualenv anytime you start developing

Clone the repo and cd into it, i.e.

```bash
git clone git@github.com:zuhairp/django-headstart.git myapp
cd myapp
```

Install dependencies
```bash
pip install -r requirements/requirements.txt
```

Start your Django project
```bash
fab project.create_project:myapp 
```

Now, get the Vagrant VM running
```bash
vagrant up
```

Next, we will set up the VM with the packages we need
```bash
fab vagrant provision
```
Or, if you're lazy (like I am)
```bash
fab v provision
```

Currently, there's an issue with how PostgreSQL is set-up, so you'll need to manually set the password (remember it)
```bash
vagrant ssh
psql vagrant_db
\password
<Follow prompts>
\q
exit
```

Next, set up the Django database in myapp/settings.py by changing the default settings (line 77 in Django 1.8)

```python
DATABASES = {
	'default' : {
    	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'vagrant_db',
        'USER' : 'vagrant',
        'PASSWORD': 'vagrant', #password you set in previous step
        'HOST': 'localhost',
        'PORT' : ''
    }
}
```

And now, you can deploy!

```bash
fab v deploy
```

To make sure things are working, you should get a Welcome to Django page at http://127.0.0.1:5000 and a message confirming Nginx is working at http://127.0.0.1:5000/welcome.html

### Continuing development
To see a list of available commands, you can run ``` fab -l ```. Here are the highlights:

#### Deployment
```fab v deploy``` runs your app's migrations and then runs Django's built in server. To use Gunicorn instead, run ```fab v deploy:gunicorn```

If you don't want to run migrations first, then you can run ```fab v runserver``` for the built in server or ```fab v gunicorn``` for Gunicorn. Either way, you can use ```fab v stop``` to stop the application server

#### Running remote manage.py commands
If you'd like to run a manage.py command against the "remote" server (whether that's Vagrant or an actual remote server), you can just do:

```bash
fab <target> manage.<command>
``` 

For example, 
```bash
fab v manage.dumpdata
```
If you want to create a fixture of the data on Vagrant's database

#### Static Files
Nginx will serve static files from the www directory of your project. Take that as you will

#### Adding other machines
You've finished your awesome app and now it's time to show it to the world! Luckily, you don't need to change your workflow too much. All you need to do is add another server to servers.config.json. Set the ```is_vagrant_vm property``` to ``` true ``` so that folder syncing is used instead of Git pulls. (Note that non-Vagrant VM code actually hasn't been written yet... I'll get to it eventually)

The properties you set will set the env for Fabric. Properties in ```config``` will apply to all servers. 

### File Structure
This is an overview of each file that comes in the repo so you know why it is there.

```bash
django-headstart
├── Vagrantfile					# Contains the config data for getting the Vagrant VM up
├── servers.config.json 		# Contains env config for all the server targets for Fabric
├── fabfile						# The fabfile module that Fabric will get its commands from
│   ├── __init__.py				# Collects all the commands and gives them nice names
│   ├── deployment.py			# Commands related to deployment: runserver, gunicorn, deploy, stop
│   ├── hosts.py				# Parses the servers.config.json and creates a Fabric task for each
│   ├── manage.py				# Creates a Fabric task for each command in manage.py
│   ├── project.py				# Fabric task for starting a new project
│   ├── provisioning.py			# Fabric task to provision the server with the proper packages
│   └── utils.py				# Utilities for getting the correct directories and stuff
├── requirements				# Contains all the requirements for the project
│   ├── requirements-dev.txt	# Requirements for development, right now just Fabric and fabtools
│   ├── requirements-prod.txt   # Requirements for actually running the app, i.e. everything not Fabric
│   └── requirements.txt		# References -dev and -prod
└── www							# Put static files in here
    └── welcome.html			# Test file to indicate Nginx reverse proxy is working
```



