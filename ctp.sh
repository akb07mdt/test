# check for updates
# assume git-bash path as default

WORKING_PATH=$(echo $0 | sed 's/\(.*\)\/[^/]*.sh$/\1/' -)
$WORKING_PATH/commit.sh
$WORKING_PATH/tp.sh

