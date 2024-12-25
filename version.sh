#sh

function check_exit {
  if [ "$1" != "0" ]; then
    echo $2
    exit 1
  fi
}


# get the name of the git repo to tag
cd Product
OUTFILE=DataBase/version.h

# generate the tag name as a project name and date stamp
TIME_STAMP=$(date --utc +%Y%m%d_%H%M%S)
REPO_NAME=TM91
PROD_DATE=$(echo $TIME_STAMP | sed 's/^\([0-9]*\)_[0-9]*/\1/' -)
PROD_TIME=$(echo $TIME_STAMP | sed 's/^[0-9]*_\([0-9]*\)/\1/' -)
PROD_VER=${REPO_NAME}_${PROD_DATE}_${PROD_TIME}
echo "Product version string is \"${REPO_NAME}_${PROD_DATE}_${PROD_TIME}\""

echo "// @file version.h" > $OUTFILE
echo "//" >> $OUTFILE
echo "// Holds Version Strings for this product." >> $OUTFILE
echo "//" >> $OUTFILE
echo "// Use the tag $PROD_VER" >> $OUTFILE
echo "//   to checkout code associated with this version." >> $OUTFILE
echo "" >> $OUTFILE
echo "#define PRODUCT_NAME    \"$REPO_NAME\"" >> $OUTFILE
echo "#define PRODUCT_DATE    \"$PROD_DATE\"" >> $OUTFILE
echo "#define PRODUCT_TIME    \"$PROD_TIME\"" >> $OUTFILE
echo "#define PRODUCT_TAG     \"$PROD_VER\"" >> $OUTFILE
echo "#define PRODUCT_VERSION \"$1\"" >> $OUTFILE
echo "" >> $OUTFILE

echo "Successfully updated version.h file"
echo "NOTE: Remember to rebuild before committing!"



