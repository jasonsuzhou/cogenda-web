#!/bin/bash
# Linode stackscript for Cogenda with Ubuntu14 distro
# Secure production env and installs a complete web environment with Ngnix, Python, Virtualenv and SQLite3 
# <UDF name="sys_hostname" label="System hostname" default="localhost" example="Name of your server, i.e. linode1." />
# <UDF name="sshd_passwordauth" label="Use SSH password authentication" oneof="Yes,No" default="No" example="Turn off password authentication if you have added a Public Key." />
# <UDF name="sshd_permitrootlogin" label="Permit SSH root login" oneof="No,Yes" default="No" example="Root account should not be exposed." />
# <UDF name="user_shell" label="Shell" oneof="/bin/zsh,/bin/bash" default="/bin/bash" />
# <UDF name="deploy_user" Label="Name of deployment user" default="deploy" />
# <UDF name="deploy_password" Label="Password for deployment user" />
# <UDF name="deploy_sshkey" Label="Deployment user public ssh key" />
# <UDF name="ssh_port" Label="SSH Port" default="22" />
# <UDF name="notify_email" Label="Send Finish Notification To" example="Email address to send notification to when finished.

USER_GROUPS=sudo

exec &> /root/stackscript.log
source <ssinclude StackScriptID=1> # Common bash functions
source <ssinclude StackScriptID=123> # Ubuntu utils script

function log {
  echo "### $1 -- `date '+%D %T'`"
}


function create_deployment_user {
  system_add_user $DEPLOY_USER $DEPLOY_PASSWORD "users,sudo"
  if [ "$DEPLOY_SSHKEY" ]; then
    system_user_add_ssh_key $DEPLOY_USER "$DEPLOY_SSHKEY"
  fi
  system_update_locale_en_US_UTF_8
  log "Added deploy user account"
}



function config_sshd {
    # Configure sshd
    system_sshd_permitrootlogin "$SSHD_PERMITROOTLOGIN"
    system_sshd_passwordauthentication "$SSHD_PASSWORDAUTH"
    touch /tmp/restart-ssh
    log "Finished configure sshd" 

    # Lock user account if not used for login
    if [ "SSHD_PERMITROOTLOGIN" == "No" ]; then
        system_lock_user "root"
        log "Locked root user account" 
    fi
}

function install_env {
    apt-get -y install logrotate
    apt-get -y install git-core 
    apt-get -y install sqlite3 libsqlite3-dev
    apt-get -y install python-dev
    apt-get -y install python-pip
    apt-get -y install python-setuptools
    pip install virtualenv
    aptitude -y install nginx
}

log "Updating System..."
system_update

log "Updating Hostname..."
system_update_hostname "$SYS_HOSTNAME"

log "Creating Deployment User: $DEPLOY_USER"
create_deployment_user 

cat >> /etc/sudoers <<EOF
Defaults !secure_path
$DEPLOY_USER ALL=(ALL) NOPASSWD: ALL
EOF

log "Make Basic Settings..."
config_sshd 
system_security_fail2ban
log "Installed fail2ban"
system_security_ufw_configure_basic
/etc/init.d/ssh restart

log "Install Dependencie Env..."
install_env 

log "Restarting Services..."
restartServices