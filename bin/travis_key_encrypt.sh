#!/bin/bash
# Encrypts private SSH keys for use in .travis.yml.
# Also see the travis documentation:
# http://docs.travis-ci.com/user/build-configuration/#Secure-environment-variables

# Usage:
# Go to your git project:
#   cd my_project
# Then run:
#   ./bin/travis_key_encrypt.sh ./etc/my_private_key

SSH_KEY_PATH=$1

#base64 --break 64 ${SSH_KEY_PATH} > ${SSH_KEY_PATH}_base64

if [[ ! $(which travis) ]]
then
  gem install travis
fi

travis login --pro --auto

for l in $(cat ${SSH_KEY_PATH});
do
  travis encrypt $l --add env.global
done
