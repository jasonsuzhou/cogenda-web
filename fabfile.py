#-*- coding:utf-8 -*-

"""
- Install dependency 
- Deploy files
- Configure Nginx 
- Restart web server
- Restart Nginx
"""

from fabric.api import *
from fabric.colors import green, red


####################################################################
# 			     Cogenda Server Auto Deployment                    #
####################################################################
# Internal variables
app_path = "/home/ubuntu/apps/cogenda-web"

def login(user, secret, host):
    """Prepare to login to production server."""
    env.user = user
    env.password= secret
    env.host_string = host
    run("uname -a")


def install():
    """
    Prepare server for installation:
    - sync with GitHub repo.
    - install upstart service
    """
    #TODO:


def nginx():
    """Configure Nginx service"""
    nginx_conf = "nginx.conf"
    path_nginx = "/etc/nginx/sites-available/"
    print(red("Configure Nginx web server"))
    with cd(path_nginx):
        run("sudo cp -f %s/etc/%s ./default" %(app_path, nginx_conf))


def restart():
    """Restart cogenda-app service & Nginx service"""
    print(green("Restarting the cogenda-app service & Nginx service..."))
    process = "cogenda-app"
    run("sudo restart %s" % process)
    run("sudo service nginx restart")
    print(red("Auto deploy cogenda web to production succeed!"))



####################################################################
# 			     Sync with AWS S3 & AliYun                         #
####################################################################
#TODO:
