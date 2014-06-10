#-*- coding:utf-8 -*-

"""
- Install dependency 
- Deploy files
- Configure Nginx 
- Restart web server
- Restart Nginx
"""

from fabric.api import *
from fabric.contrib.files import exists
from fabric.colors import green, red
####################################################################
# 			     Cogenda App Auto Deployment                       #
####################################################################

# Internal variables
app_path = "/home/tim/apps"
cogenda_web_path = "/home/tim/apps/cogenda-web"
travis_ssh_key = "~/.ssh/id_rsa_deploy"
deploy_user="tim"
deploy_host="85.159.208.213"

def prepare():
    """Prepare to login to production server."""
    env.host_string = deploy_host 
    env.user = deploy_user
    env.key_filename = travis_ssh_key
    env.port = 22


def install_app():
    """
    Prepare server for installation:
    - install upstart service
    """
    if exists(cogenda_web_path):
        with cd(cogenda_web_path):
            run("git pull -f origin master")
    else:
        with cd(app_path):
            run("git clone https://github.com/cogenda/cogenda-web.git")

def install_upstart():
    """ Install upstart service """
    upstart_path = "/etc/init"
    with cd(cogenda_web_path):
        run("sudo cp -f etc/cogenda-app.conf %s" %(upstart_path))
    print(red("Auto configure upstart succeed!"))


def nginx():
    """Configure Nginx service"""
    nginx_conf_path = "%s/etc/nginx.conf" %(cogenda_web_path)
    path_nginx = "/etc/nginx/sites-available/"
    print(green("Configure Nginx web server"))
    with cd(path_nginx):
        run("sudo cp -f %s ./default" %(nginx_conf_path))
    print(red("Auto configure Nginx server succeed!"))


def restart():
    """Restart cogenda-app service & Nginx service"""
    print(green("Restarting the cogenda-app service & Nginx service..."))
    #process = "cogenda-app"
    #run("sudo restart %s" % process)
    with cd("%s/bin/" %(cogenda_web_path)):
        run("./bootstrap.sh")
    run("sudo service nginx restart")
    print(red("Auto deploy cogenda web to production succeed!"))
