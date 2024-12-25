#sh

function check_exit {
  if [ "$1" != "0" ]; then
    echo $2
    exit 1
  fi
}

# $1 is the name of the folder with the repo to commit
# $2 is the name of the commit text file
function commit_repo {
  git commit --all --file=$1
}

REPO_NAME=TM91
# get a temporary file to store the commit message in
TMP_FILE=$(mktemp --tmpdir=.)
TMP_FILE=$(readlink -f $TMP_FILE)
echo "TMP_FILE = $TMP_FILE"

check_exit $? "Unable to create temporary file for commit message"
  
# fill the temporary file with the commit prompts
echo -e "<Provide a commit title here for project $REPO_NAME>\r\n\r\n<Replace this text with commit details and then save and exit the editor>" > $TMP_FILE
  
# present the temporary file to the user for editing
if [ "$(which notepad)" != "" ]; then
  # remove cygdrive if it exists then update drive letter to point to dos drive with :
  # and finally update forward slashes to backward slashes
  notepad $(echo $TMP_FILE | sed 's/\/cygdrive// ; s/\/\(.\)/\1:/ ; s/\//\\/g')
else
  vi $TMP_FILE
fi


if (( $? != 0 )); then

  echo "Editor exited without save, Commit aborted."

elif [ "$(grep 'Provide a commit title here' $TMP_FILE)" != "" ]; then

  echo "Please modify the commit message before saving the file."

else
  commit_repo $TMP_FILE
fi

# lastly, remove the temporary file used for commit comments
rm $TMP_FILE
  

