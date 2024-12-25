#sh

# run release.sh from /Releases directory with just the tag being released.

# $1 is the *.hex file to copy
# $2 is the directory to copy to
# $3 is the tag to append
function copy_with_tag {
  for file in $1/*.hex; do
    TO_FILE=$(echo $file | sed "s/src\/.*\/Exe\/\([^.]*\)\.hex/\1_$3\.hex/" -)
    cp $file $2/$TO_FILE;
  done
}

# check for updates
# assume git-bash path as default
SCRIPTS_DIR=/j/Groups/Instruments/Tikos/Scripts
# check to see if cygwin path is required
OS_NAME=$(uname)
if [ "${OS_NAME:0:6}" == "CYGWIN" ]; then
  SCRIPTS_DIR=/cygdrive$SCRIPTS_DIR
fi
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

WORKING_PATH=$(dirname $(realpath $0))
PROJECT_NAME=$(echo $1 | sed 's/\([^_]*\).*/\1/' -)

mkdir --parents $PROJECT_NAME/$1
cd $PROJECT_NAME/$1

$WORKING_PATH/clone.sh $PROJECT_NAME src $1

mkdir hex

if [ "$PROJECT_NAME" == "WR9200BB05" ] || [ "$PROJECT_NAME" == "WR9210BB05" ] || [ "$PROJECT_NAME" == "WR9220BB05" ]; then
  copy_with_tag src/Product/Output/Debug/Exe hex $1
  copy_with_tag src/Recharge/Output/Debug/Exe hex $1
  copy_with_tag src/TelN/Output/Debug/Exe hex $1
  copy_with_tag src/UI/Output/Debug/Exe hex $1
fi

if [ "$PROJECT_NAME" == "IndraBB03" ]; then
  copy_with_tag src/Product/Output/Debug/Exe/ hex $1
fi

if [ "$PROJECT_NAME" == "IndraBB04" ]; then
  copy_with_tag src/Product/Output/Debug/Exe/ hex $1
  copy_with_tag src/UITelN/Output/Debug/Exe hex $1
fi

if [ "$PROJECT_NAME" == "MaverickBB01" ]; then
  copy_with_tag src/Product/Output/Debug/Exe hex $1
fi

