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

def setup(user, secret, host):
    """Prepare to login to production server."""
    env.user = user
    env.password= secret
    env.host_string = host
    run("uname -a")
