# On Linux (tested only on Ubuntu), use this script to generate secure deployment key

# To generate secure SSH deploy key for a github repo to be used from Travis
base64 --wrap=0 ~/.ssh/id_rsa_deploy > ~/.ssh/id_rsa_deploy_base64
ENCRYPTION_FILTER="echo \$(echo \"- secure: \")\$(travis encrypt \"\$FILE='\`cat $FILE\`'\" -r cogenda/cogenda-web)"
split --bytes=100 --numeric-suffixes --suffix-length=2 --filter="$ENCRYPTION_FILTER" ~/.ssh/id_rsa_deploy_base64 id_rsa_

# To reconstitute the private SSH key from within the Travis-CI build (typically from 'before_script')
#echo -n $id_rsa_{00..30} >> ~/.ssh/id_rsa_base64
#base64 --decode --ignore-garbage ~/.ssh/id_rsa_base64 > ~/.ssh/id_rsa
#chmod 600 ~/.ssh/id_rsa
#echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
