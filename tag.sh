#sh

TAG_NAME=$(grep PRODUCT_TAG Product/DataBase/version.h | sed 's/^[^"]*"\([^"]*\)"/\1/' -)
VERSION=$(grep PRODUCT_VERSION Product/DataBase/version.h | sed 's/^[^"]*"\([^"]*\)"/\1/' -)


REPO_NAME=TM91

function check_exit {
  if [ "$1" != "0" ]; then
    echo $2
    exit 1
  fi
}


# $1 is the name of the tagging annotation text file
# $2 is the name of the tag
function tag_repo {
  echo -e "\ntagging $(git remote get-url --push origin)"
  git tag --annotate --file=$1 $2
}

TAG_NAME=$(grep PRODUCT_TAG Product/DataBase/version.h | sed 's/^[^"]*"\([^"]*\)"/\1/' -)
VERSION=$(grep PRODUCT_VERSION Product/DataBase/version.h | sed 's/^[^"]*"\([^"]*\)"/\1/' -)
# get a temporary file to store the annotated tag in
TMP_FILE=$(mktemp --tmpdir=.)
TMP_FILE=$(readlink -f $TMP_FILE)
echo "TMP_FILE = $TMP_FILE"

check_exit $? "Unable to create temporary file for tag annotation"
  
# fill the temporary file with the commit prompts
echo -e "Annotation for tag $TAG_NAME\r\nassociated with version $VERSION of product $REPO_NAME\r\n\r\n<Provide tag annotation details and then save and exit the editor>" > $TMP_FILE
  
# present the temporary file to the user for editing
if [ "$(which notepad)" != "" ]; then
  # remove cygdrive if it exists then update drive letter to point to dos drive with :
  # and finally update forward slashes to backward slashes
  notepad $(echo $TMP_FILE | sed 's/\/cygdrive// ; s/\/\(.\)/\1:/ ; s/\//\\/g')
else
  vi $TMP_FILE
fi


if (( $? != 0 )); then

  echo "Editor exited without save, Tagging operation aborted."

elif [ "$(grep 'Provide tag annotation details' $TMP_FILE)" != "" ]; then

  echo "Please modify the tag annotation before saving the file."

else
  echo "Tagging as $TAG_NAME"
  cat $TMP_FILE
  echo "tag_repo $TMP_FILE $TAG_NAME"
  tag_repo $TMP_FILE $TAG_NAME
fi

# lastly, remove the temporary file used for tag annotation
rm $TMP_FILE
  

