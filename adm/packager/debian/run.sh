#!/bin/bash
#
#Usage example:
# sudo ./run.sh   0.37.1  0
#
# ASSUMPTION: -- sources have been copied to /tmp/quex-$VERSION
#             -- /tmp/quex-packages exists
#
# ORIGINAL AUTHOR: Joaquin Duo, joaduo at users sourceforge net
# MODIFIED BY:     Frank-Rene Schaefer, fschaef at users sourceforge net
#
#-----------------------------------------------------------------------
VERSION=$1
PACKAGE_VERSION=$2

#Config
BIN_DIRECTORY='/usr/local/bin'

#sudo does not seem to inherit path files
echo "QUEX_PATH: $QUEX_PATH"
if [ "$QUEX_PATH" = "" ]; then
    echo "Assume QUEX_PATH = current path!"
    export QUEX_PATH=$PWD
fi
if [[ $# < 1 ]]; then
    echo "Please, review the text content of this script for usage information."
    exit 1
fi
if [[ $# == 1 ]]; then
    PACKAGE_VERSION="0"
fi

#Create the variables after checking the inputs
dir_base=/tmp/quex-$VERSION
dir_template=$QUEX_PATH/adm/packager/debian/scripts/
dir_package=/tmp/"quex_$VERSION-$PACKAGE_VERSION""_all"

# Check assumption that sources are copied to /tmp/quex-$VERSION
if test ! -e $dir_base; then
# else
    echo "/tmp/quex-$VERSION must exist before calling this script."
    exit 1
fi

#Create the dir_package with the DEBIAN control directory
mkdir -p $dir_package/DEBIAN

# Update the version and package information in:
#  -- control file
#  -- post install file
#  -- pre-remove file
#  -- post remove file
BIN_DIRECTORY_REPLACE=$( echo $BIN_DIRECTORY | sed 's/\//\\\//g')
scripts="control preinst postinst prerm postrm copyright"
for script in $scripts; do
      sed "s/##QUEX_VERSION/$VERSION/" $dir_template/$script | \
      sed "s/##PACKAGE_VERSION/$PACKAGE_VERSION/" | \
      sed "s/##BIN_DIRECTORY/$BIN_DIRECTORY_REPLACE/"  > \
      $dir_package/DEBIAN/$script
      chmod 0755 $dir_package/DEBIAN/$script
done

#Copy the manpage into manpage.*
cp $dir_base/doc/manpage/quex.1 $dir_package/DEBIAN/manpage.1

#Copy sources to the new destination on package
mkdir -p $dir_package/opt/quex/quex-$VERSION
sudo cp -a $dir_base/* $dir_package/opt/quex/quex-$VERSION

#Set file owners
#Need to be root for this by now, later ill use fakeroot
sudo chown root:root -R $dir_package/opt

# Create the package
sudo dpkg-deb -b $dir_package

# Make package accessible 
sudo chmod 777 /tmp/*.deb 

# Verify existence in package directory
ls -l /tmp/*.deb
exit 0
