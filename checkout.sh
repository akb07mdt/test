#sh

CYAN='\033[0;36m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
STOP_CLR='\033[0m'

# get the sha-1 of the current head
SHA1=$(git rev-parse HEAD)

# get the list of branches associated with this sha-1
BRANCHES=($(git branch --remotes --points-at $SHA1 | sed '/HEAD/d ; s/^.*\///'))

# default branch is the only branch
BRANCH_SEL=0

# see if more than one branch exists
if [ $(( ${#BRANCHES[@]} != 1 )) -ne 0 ]; then

  # more than one branch exists, loop until the user provides a valid response
  MENU_FLAG="True"
  while [ $MENU_FLAG == "True" ]; do

    # provide a menu for the user and get input
    echo -e "${GREEN}Available Branches:${STOP_CLR}"
    for i in $( seq 0 $(( ${#BRANCHES[@]} - 1 )) ); do
      echo -e "${CYAN}$i${STOP_CLR} - ${YELLOW}${BRANCHES[$i]}${STOP_CLR}"
    done
    echo -en "${CYAN}"
    read -p "Selected Branch: " BRANCH_SEL
    echo -en "${STOP_CLR}"

    # See if the user input is valid
    if [ $(( BRANCH_SEL >= 0 && BRANCH_SEL < ${#BRANCHES[@]} )) -ne 0 ]; then
      MENU_FLAG="False" # user input valid, exit loop
    else
      # user input invalid, prompt with error and retry the loop
      echo
      echo -e "${RED}Input value of $BRANCH_SEL is out of range.  Retry...${STOP_CLR}"
    fi

  done

  # warm fuzzies
  echo -e "${MAGENTA}Using branch '${BRANCHES[$BRANCH_SEL]}'${STOP_CLR}"

fi

# effect the checkout of the branch selected or the only branch available
git checkout ${BRANCHES[$BRANCH_SEL]}

