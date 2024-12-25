# check for updates
SCRIPTS_DIR=/j/Groups/Instruments/Tikos/Scripts
RUN_DIR=$(dirname $(readlink -f $0))
OPERATION=$(echo $(basename $(readlink -f $0)) | sed 's/\.sh//' -)
if [ -f "$SCRIPTS_DIR/$OPERATION.sh" ]; then
  if [ "$RUN_DIR" != "$SCRIPTS_DIR" ]; then
    if [ "$(diff $RUN_DIR/$OPERATION.sh $SCRIPTS_DIR/$OPERATION.sh 2>&1)" != "" ]; then
      read -p "You do not have the latest $OPERATION script, do you want to update it? " CHOICE
      CHOICE=${CHOICE:-N}   # assign default value if not assigned
      CHOICE=${CHOICE^^}    # force upper case results
      if [ "${CHOICE:0:1}" == "Y" ]; then # only check first character
        cp -f $SCRIPTS_DIR/$OPERATION.sh $RUN_DIR/$OPERATION.sh
        $SCRIPTS_DIR/$OPERATION.sh $*
        exit $?
      fi
    fi
  fi
fi

if [ "$1" == "" ]; then
  echo "To push you must supply a valid user id for gerrit, i.e. smithj2"
fi

WORKING_PATH=$(echo $0 | sed 's/\(.*\)\/[^/]*.sh$/\1/' -)

$WORKING_PATH/commit.sh
$WORKING_PATH/push.sh $1

