#!/bin/bash
# Encrypts private travis ci env var for use in .travis.yml.
# Also see the travis documentation:
# http://docs.travis-ci.com/user/build-configuration/#Secure-environment-variables

# Usage:
# Go to your git project:
#   cd my_project
# Then run:
#   ./bin/travis_key_encrypt.sh ./etc/travis_env.txt
ENV_KEY_PATH=$1

#base64 --break 64 ${ENV_KEY_PATH} > ${ENV_KEY_PATH}_base64

if [[ ! $(which travis) ]]
then
  gem install travis
fi

travis login --pro --auto

for l in $(cat ${ENV_KEY_PATH});
do
  travis encrypt $l --add env.global
done


