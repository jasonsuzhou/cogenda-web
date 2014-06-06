#-*- coding:utf-8 -*-

"""
- Install dependency 
- Deploy files
- Configure Nginx 
- Restart web server
"""

from fabric.api import *
from fabric.colors import green, red

def setup(secret, host, user='root'):
    """Prepare to login to production server."""
    env.host_string = host
    env.user = user
    env.password= secret
    run("uname -a")
