#!/bin/bash
# Linode stackscript for Cogenda with Ubuntu14 distro
# Secure production env and installs a complete web environment with Ngnix, Python, Virtualenv and SQLite3 
# <UDF name="sys_hostname" label="System hostname" default="localhost" example="Name of your server, i.e. linode1." />
# <UDF name="sshd_passwordauth" label="Use SSH password authentication" oneof="Yes,No" default="No" example="Turn off password authentication if you have added a Public Key." />
# <UDF name="sshd_permitrootlogin" label="Permit SSH root login" oneof="No,Yes" default="No" example="Root account should not be exposed." />
# <UDF name="user_shell" label="Shell" oneof="/bin/zsh,/bin/bash" default="/bin/bash" />
# <UDF name="deploy_user" Label="Name of deployment user" default="deploy" />
# <UDF name="deploy_password" Label="Password for deployment user" default="deploy" />
# <UDF name="deploy_sshkey" Label="Deployment user public ssh key" />
# <UDF name="smtp_password" Label="Cogenda mail server password" />
# <UDF name="cogenda_shared_secret" Label="Cogenda webserice HMAC based shared key" default="cogenda-ws-secret" />
# <UDF name="ssh_port" Label="SSH Port" default="22" />
# <UDF name="notify_email" Label="Send Finish Notification To" example="Email address to send notification to when finished." />

source <ssinclude StackScriptID=1> # https://www.linode.com/stackscripts/view/1
source <ssinclude StackScriptID=123> # https://www.linode.com/stackscripts/view/123

USER_GROUPS=sudo

exec &> /root/stackscript.log

export SMTP_PASSWORD="$SMTP_PASSWORD"
export COGENDA_SHARED_SECRET="$COGENDA_SHARED_SECRET"

function create_deployment_user {
  system_add_user $DEPLOY_USER $DEPLOY_PASSWORD "users,sudo"
  if [ "$DEPLOY_SSHKEY" ]; then
    system_user_add_ssh_key $DEPLOY_USER "$DEPLOY_SSHKEY"
  fi
  system_update_locale_en_US_UTF_8
  echo "Added deploy user account"
}


function system_tunning{
  echo "Tunning system settings..."
  update-alternatives --set editor /usr/bin/vim
  sed -i 's/X11Forwarding yes/X11Forwarding no/g' /etc/ssh/sshd_config
  sed -i 's/UsePAM  yes/UsePAM no/g' /etc/ssh/sshd_config
  # Configure sshd
  system_sshd_permitrootlogin "$SSHD_PERMITROOTLOGIN"
  system_sshd_passwordauthentication "$SSHD_PASSWORDAUTH"
  # Disable root user account if not used for login
  if [ "SSHD_PERMITROOTLOGIN" == "No" ]; then
      system_lock_user "root"
      echo "Locked root user account" 
  fi
  echo "Finished configure sshd" 
}


function install_env {
    apt-get -y install git-core 
    apt-get -y install sqlite3 libsqlite3-dev
    apt-get -y install python-dev
    apt-get -y install python-pip
    apt-get -y install python-setuptools
    pip install virtualenv
}

function install_nginx_with_geoip {
    aptitude -y install nginx
    mkdir -p /etc/nginx/geoip
    cd /etc/nginx/geoip
    wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
    gunzip GeoIP.dat.gz
}

function install_node {
    wget http://nodejs.org/dist/v0.10.22/node-v0.10.22.tar.gz 
    tar -xvzf node-v0.10.22.tar.gz
    cd node-v0.10.22
    ./configure
    make
    sudo make install
}

echo "Updating System..."
system_update

echo "Updating Hostname..."
system_update_hostname "$SYS_HOSTNAME"

echo "Creating Deployment User: $DEPLOY_USER"
create_deployment_user 

cat >> /etc/sudoers <<EOF
Defaults !secure_path
$DEPLOY_USER ALL=(ALL) NOPASSWD: ALL
EOF

echo "Make Basic Settings..."
system_tunning 

service ssh reload

echo "Install Dependencie Env..."
install_env 

echo "Install NodeJS..."
install_node

echo "Install nginx..."
install_nginx_with_geoip

echo "Restarting Services..."
restart_services
restart_initd_services

echo "Finished..."
