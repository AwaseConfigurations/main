#!/bin/bash

# This is a script for building simple configuration packages.
# Copyright 2011 Henri Siponen
# License: GNU General Public License, version 2 or later
# More help can be found here: http://awaseconfigurations.wordpress.com/2011/10/02/config-package-dev-building-configuration-packages/

# Uncomment the lines below to install config-package-dev and rest of the needed packages
#sudo apt-get install config-package-dev
#sudo apt-get install build-essential cdbs debhelper wdiff debian-el devscripts devscripts-el dh-make dpatch dpkg-awk dpkg-dev dpkg-dev-el equivs fakeroot lintian quilt sbuild gdebi

echo ""
echo "################################################"
echo "Type the name of your package: "
read name

mkdir "$name"
cd "$name"
mkdir debian
cd debian

echo "$name (0.1) unstable; urgency=low" >> changelog
echo "" >> changelog
echo "  * Initial release." >> changelog
echo "" >> changelog
echo " -- Henri Siponen <hng.siponen@gmail.com>  $(date -R)" >> changelog

echo "5" >> compat

echo "Source: $name" >> control
echo "Section: config" >> control
echo "Priority: extra" >> control
echo "Maintainer: Henri Siponen <hng.siponen@gmail.com>" >> control
echo "Build-Depends: cdbs (>= 0.4.23-1.1), debhelper (>= 4.2.0), config-package-dev (>= 4.5~)" >> control
echo "Standards-Version: 3.8.0" >> control
echo "" >> control
echo "Package: $name" >> control
echo "Architecture: all" >> control
echo "Depends: cdbs, \${misc:Depends}" >> control
echo "Provides: \${diverted-files}" >> control
echo "Conflicts: \${diverted-files}" >> control
echo "Description: This is a config package" >> control

echo "Source: $name" >> control.in
echo "Section: config" >> control.in
echo "Priority: extra" >> control.in
echo "Maintainer: Henri Siponen <hng.siponen@gmail.com>" >> control.in
echo "Build-Depends: @cdbs@" >> control.in
echo "Standards-Version: 3.8.0" >> control.in
echo "" >> control.in
echo "Package: $name" >> control.in
echo "Architecture: all" >> control.in
echo "Depends: cdbs, \${misc:Depends}" >> control.in
echo "Provides: \${diverted-files}" >> control.in
echo "Conflicts: \${diverted-files}" >> control.in
echo "Description: This is a config package" >> control.in

echo "Copyright 2011 Henri Siponen" >> copyright
echo "License: GNU General Public License, version 2 or later" >> copyright

echo "Type the path to the config file(eg. /etc/deluser.conf): "
read path

echo "#!/usr/bin/make -f" >> rules
echo "" >> rules
echo "DEB_DIVERT_EXTENSION = .hng" >> rules
echo "DEB_TRANSFORM_FILES_$name += $path.hng" >> rules
echo "" >> rules
echo "include /usr/share/cdbs/1/rules/debhelper.mk" >> rules
echo "include /usr/share/cdbs/1/rules/config-package.mk" >> rules

echo "Type the name of the config file(eg. deluser.conf): "
read file

echo "#!/usr/bin/perl -0p" >> transform_"$file".hng
echo "s/^# (.*bonobo.*)/\$1/m;" >> transform_"$file".hng
echo "s/^(mango.*banana)/# \$1/m;" >> transform_"$file".hng

echo ""
echo "New config package $name created."
echo ""
echo "Edit $name/debian/transform_$file.hng for your config needs."
echo "Then build with this command: dpkg-buildpackage -rfakeroot"
echo -n "And install with this: sudo gdebi -n $name"
echo "_0.1_all.deb"
echo ""
