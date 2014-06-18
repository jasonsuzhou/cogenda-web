#-*- coding:utf-8 -*-

"""
Cogenda web application auto deployment tool.
- Pull latest code from github.
- Install dependency.
- Configure cogenda app & Nginx settings.
- Restart cogenda app server & Nginx server.
"""

from fabric.api import *
from fabric.contrib.files import exists
from fabric.colors import green, red
from contextlib import contextmanager as _contextmanager
####################################################################
# 			     Cogenda App Auto Deployment                       #
####################################################################

# Internal variables
APP_PATH = "/home/tim/apps"
COGENDA_HOME = "%s/cogenda-web" %(APP_PATH)
COGENDA_REPO="https://github.com/cogenda/cogenda-web.git"
COGENDA_DB="%s/migration/cogenda-app.db" %(COGENDA_HOME)
DEPLOY_USER="tim"
DEPLOY_HOST="85.159.208.213"
TRAVIS_SSH_KEY = "~/.ssh/id_rsa"
PID_FILE="/tmp/cogenda-app.pid"
ENV_ACTIVATE="source venv/bin/activate"
NGINX_CLOUD_CONF="nginx.cloud.conf"
NGINX_LOCAL_CONF="nginx.local.conf"

@_contextmanager
def virtualenv():
    with cd(COGENDA_HOME):
        with prefix(ENV_ACTIVATE):
            yield

            
def prepare():
    """Prepare to login to production server."""
    env.host_string = DEPLOY_HOST 
    env.user = DEPLOY_USER
    env.key_filename = TRAVIS_SSH_KEY
    env.port = 22
    print(red("Login Cogenda production server succeed!"))


def install_app():
    """
    Prepare server for installation:
    - make app location
    - install db-migrate
    - install dependency libs
    """
    if not exists(APP_PATH):
        run("mkdir -p %s" %(APP_PATH))

    if exists(COGENDA_HOME):
        with cd(COGENDA_HOME):
            run("git pull -f origin master")
    else:
        with cd(APP_PATH):
            run("git clone %s" %(COGENDA_REPO))
    with cd(COGENDA_HOME):
        run("./setenv.sh")
    print(red("Auto install cogenda app succeed!"))


def migrate_db():
    with virtualenv():
        with cd(COGENDA_HOME):
            if exists(COGENDA_DB):
                run("make db-migrate")
            else:
                run("make db-init")
    print(red("Auto db migration succeed!"))


def restart_app():
    with virtualenv():
        run("ps -ef | grep 'cogenda-app' | grep -v 'grep' | awk '{print $2}' | xargs kill -9")
        with cd(COGENDA_HOME):
            run("make run-prod")
    print(red("Restart Cogenda App succeed!"))
    

def restart_nginx():
    """Configure Nginx service"""
    nginx_conf_path = "%s/etc/%s" %(COGENDA_HOME, NGINX_CLOUD_CONF)
    path_nginx = "/etc/nginx/sites-available/"
    print(green("Configure Nginx web server"))
    with cd(path_nginx):
        run("sudo cp -f %s ./default" %(nginx_conf_path))
    run("sudo service nginx restart")
    print(red("Auto configure & restart Nginx server succeed!"))
    print(green("Auto deploy to production server successfully!"))
