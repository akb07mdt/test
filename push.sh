#sh

REPO_NAME=TM91

function check_exit {
  if [ "$1" != "0" ]; then
    echo $2
    exit 1
  fi
}

# $1 is the name of the folder with the repo to commit
function push_repo {
  # detect the current branch of the commit
  BRANCH=$(git branch | grep '*' - | sed 's/*// ; s/ //g' -)

  # get the push url from the origin url
  PUSH_URL=$(git remote get-url --push origin)

  # push the previously committed repo to gerrit
  git push --tags $PUSH_URL $BRANCH
}
push_repo

