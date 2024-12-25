PROJECT_NAME=$1    # The name of the project to clone
DIRECTORY_NAME=$2  # The name of the directory to clone into
TAG_NAME=$3        # The name of the tag to checkout after the clone operation

echo "Cloning $PROJECT_NAME into directory $DIRECTORY_NAME"



# checks the exit status and prints a failure string if it is non-zero then exits
function check_exit {
  EXIT_STATUS=$1  # first parameter of function call
  FAIL_STRING=$2  # second parameter of function call
  if [ "$EXIT_STATUS" != 0 ]; then
    echo $FAIL_STRING
    exit 1
  fi
}



# clone the given project into the given directory and checkout the tag/branch if given
function clone_it {
  PROJECT_TO_CLONE=$1       # first parameter of function call
  DIRECTORY_TO_CLONE_TO=$2  # second parameter of function call
  CHECKOUT=$3               # third parameter of function call

  # clone the repo to the directory defined
  echo
  echo "cloning $PROJECT_TO_CLONE into directory $DIRECTORY_TO_CLONE_TO"
  git clone git@github.com:NeuroOne/PCD-Tikos-$PROJECT_TO_CLONE.git $DIRECTORY_TO_CLONE_TO
  check_exit $? "Clone of $CHECKOUT failed"

  # change to directory just cloned to
  cd $DIRECTORY_TO_CLONE_TO
  check_exit $? "Unable to change to directory $DIRECTORY_TO_CLONE_TO"

  # default to checkout master branch if no tag is given
  if [ "$CHECKOUT" == "" ]; then
    CHECKOUT=master
  fi

  # replace any '.' with '\.' so that in subsequent expansion the period is not lost
  PATTERN=$(echo "$CHECKOUT" | sed 's/\./\\\./g' -)

  # search the repo for all tags and branches, do this quietly so it is easy to parse.
  TAGS_FOUND=$(git ls-remote --tags --heads --quiet | grep -E "/${PATTERN}$" -)

  # if tags were found...
  if [ "$TAGS_FOUND" != "" ]; then
    # checkout the tag we found
    echo "Checking out $CHECKOUT"
    git checkout --quiet $CHECKOUT
    check_exit $? "Unable to chekcout $CHECKOUT"
  else
    # if no tags were found, indicate what the default branch is
    echo "Could not find tag/branch $CHECKOUT in repo."
    echo "using branch $(git branch --list --quiet | grep '*' - | sed 's/\* //' -)"
  fi

  # return to previous directory
  cd -
  check_exit $? "Unable to return to previous directory"
}


# creates a directory with parents and them moves to it
function create_dir {
  echo
  echo "Creating directory $1"

  # create the directory
  mkdir --parents $1
  check_exit $? "Unable to create directory $1"

  # move to the newly created directory
  cd $1
  check_exit $? "Unable to change to directory $1"
}


# check for updates
# assume git-bash path as default
SCRIPTS_DIR=/j/Groups/Instruments/Tikos/Scripts
# check to see if cygwin path is required and prepend it if needed
OS_NAME=$(uname)
if [ "${OS_NAME:0:6}" == "CYGWIN" ]; then
  SCRIPTS_DIR=/cygdrive$SCRIPTS_DIR
fi
# get the directory path of where the script was run from
RUN_DIR=$(dirname $(readlink -f $0))
# get the name of the script being run less the .sh extension
OPERATION=$(echo $(basename $(readlink -f $0)) | sed 's/\.sh//' -)
if [ -f "$SCRIPTS_DIR/$OPERATION.sh" ]; then # validate we have a valid file name
  if [ "$RUN_DIR" != "$SCRIPTS_DIR" ]; then # if not running from the j drive directly
    # if file on J drive is different than the one that is running currently
    if [ "$(diff $RUN_DIR/$OPERATION.sh $SCRIPTS_DIR/$OPERATION.sh 2>&1)" != "" ]; then
      # files are different, offer update option to user
      read -p "You do not have the latest $OPERATION script, do you want to update it? " CHOICE
      CHOICE=${CHOICE:-N}   # assign default value if not assigned
      CHOICE=${CHOICE^^}    # force upper case results
      if [ "${CHOICE:0:1}" == "Y" ]; then # only check first character
        # yes, the user wants to update the script so copy it down from the J drive
        cp -f $SCRIPTS_DIR/$OPERATION.sh $RUN_DIR/$OPERATION.sh
        $SCRIPTS_DIR/$OPERATION.sh $*
        exit $?
      fi
    fi
  fi
fi


# sanity check for proper parameters
if [ "$#" != "2" ] && [ "$#" != "3" ]; then
  echo "Usage:"
  echo "$0 <Project> <Directory> [<tag-branch>]"
  echo "   where:"
  echo "   <Project>    name of the Git repository project for the product."
  echo "   <Directory>  directory path to clone into."
  echo "   <tag-branch> optional tag or branch to checkout, defaults to master."
  exit 1
fi


# create the directory to clone the project set into
if [ ! -d $DIRECTORY_NAME ]; then
  create_dir $DIRECTORY_NAME
else
  cd $DIRECTORY_NAME
fi


if [ "$PROJECT_NAME" == "WR9200BB07" ]; then
  clone_it Product-$PROJECT_NAME Product $TAG_NAME
  clone_it Common Common $TAG_NAME
  clone_it BLEFirmware BLE $TAG_NAME
  clone_it Tools Tools $TAG_NAME
  
  clone_it WR9200Bootloader WR9200Bootloader $TAG_NAME
  
  clone_it Recharge-BB07 Recharge $TAG_NAME
  clone_it TelN-BB07 TelN $TAG_NAME
  clone_it UI-BB07 UI $TAG_NAME

  create_dir Platform
  clone_it Platform-F423 F423 $TAG_NAME
  clone_it Platform-L432 L432 $TAG_NAME
fi


if [ "$PROJECT_NAME" == "IndraChar_1_6" ]; then
  clone_it Product-$PROJECT_NAME Product $TAG_NAME
  clone_it Common Common $TAG_NAME
  clone_it Tools Tools $TAG_NAME
  clone_it BLEFirmware BLE $TAG_NAME
  
  clone_it IndraBootloader IndraBootloader $TAG_NAME
  
  clone_it UITelN UITelN $TAG_NAME

  create_dir Platform
  clone_it Platform-F423 F423 $TAG_NAME
  clone_it Platform-L432 L432 $TAG_NAME
fi


if [ "$PROJECT_NAME" == "MaverickBeethoven" ]; then
  clone_it Product-$PROJECT_NAME Product $TAG_NAME
  clone_it Common Common $TAG_NAME
  clone_it BLEFirmware BLE $TAG_NAME
  clone_it Tools Tools $TAG_NAME
  
  clone_it MaverickBootloader MaverickBootloader $TAG_NAME
  
  clone_it Recharge-SC Recharge-SC $TAG_NAME
  clone_it TelN-SC TelN-SC $TAG_NAME
  clone_it UI-SC UI-SC $TAG_NAME

  create_dir Platform
  clone_it Platform-F423 F423 $TAG_NAME
  clone_it Platform-L432 L432 $TAG_NAME
fi


# Old Hardware
if [ "$PROJECT_NAME" == "WR9200BB05" ]; then
  clone_it Product-$PROJECT_NAME Product $TAG_NAME
  clone_it Common Common $TAG_NAME
  clone_it BLEFirmware BLE $TAG_NAME
  clone_it Tools Tools $TAG_NAME
  
  clone_it Recharge Recharge $TAG_NAME
  clone_it TelN TelN $TAG_NAME
  clone_it UI UI $TAG_NAME

  create_dir Platform
  clone_it Platform-F423 F423 $TAG_NAME
  clone_it Platform-L432 L432 $TAG_NAME
fi


if [ "$PROJECT_NAME" == "IndraBB03" ]; then
  clone_it Product-$PROJECT_NAME Product $TAG_NAME
  clone_it Common Common $TAG_NAME
  clone_it Tools Tools $TAG_NAME
  clone_it BLEFirmware BLE $TAG_NAME

  create_dir Platform
  clone_it Platform-F423 F423 $TAG_NAME
fi


if [ "$PROJECT_NAME" == "IndraBB04" ]; then
  clone_it Product-$PROJECT_NAME Product $TAG_NAME
  clone_it Common Common $TAG_NAME
  clone_it Tools Tools $TAG_NAME
  clone_it BLEFirmware BLE $TAG_NAME
  
  clone_it UITelN UITelN $TAG_NAME

  create_dir Platform
  clone_it Platform-F423 F423 $TAG_NAME
  clone_it Platform-L432 L432 $TAG_NAME
fi


echo
echo "Successfully cloned the $PROJECT_NAME project into directory $DIRECTORY_NAME"

