#!/bin/bash

# This is a script for building simple configuration packages.
# It uses DEB_TRANSFORM_FILES and DEB_DIVERT_EXTESION from config-package-dev
# to replace config file with a symlink to a modified version of the file.
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

cat > changelog << EOF
$name (0.1) unstable; urgency=low

  * Initial release.

 -- Henri Siponen <hng.siponen@gmail.com>  $(date -R)
EOF

echo "5" >> compat

cat > control << EOF
Source: $name
Section: config
Priority: extra
Maintainer: Henri Siponen <hng.siponen@gmail.com>
Build-Depends: cdbs (>= 0.4.23-1.1), debhelper (>= 4.2.0), config-package-dev (>= 4.5~)
Standards-Version: 3.8.0

Package: $name
Architecture: all
Depends: cdbs, \${misc:Depends}
Provides: \${diverted-files}
Conflicts: \${diverted-files}
Description: This is a config package
EOF

cat > control.in << EOF
Source: $name
Section: config
Priority: extra
Maintainer: Henri Siponen <hng.siponen@gmail.com>
Build-Depends: @cdbs@
Standards-Version: 3.8.0

Package: $name
Architecture: all
Depends: cdbs, \${misc:Depends}
Provides: \${diverted-files}
Conflicts: \${diverted-files}
Description: This is a config package
EOF

cat > copyright << EOF
Copyright 2011 Henri Siponen
License: GNU General Public License, version 2 or later
EOF

echo "Type the path to the config file(eg. /etc/deluser.conf): "
read path

cat > rules << EOF
#!/usr/bin/make -f

DEB_DIVERT_EXTENSION = .hng
DEB_TRANSFORM_FILES_$name += $path.hng

include /usr/share/cdbs/1/rules/debhelper.mk
include /usr/share/cdbs/1/rules/config-package.mk
EOF

echo "Type the name of the config file(eg. deluser.conf): "
read file

cat > transform_"$file".hng << EOF
#!/usr/bin/perl -0p
s/^# (.*bonobo.*)/\$1/m;
s/^(mango.*banana)/# \$1/m;
EOF

echo ""
echo "New config package $name created."
echo ""
echo "Edit $name/debian/transform_$file.hng for your config needs."
echo "Then build with this command: dpkg-buildpackage -rfakeroot"
echo -n "And install with this: sudo gdebi -n $name"
echo "_0.1_all.deb"
echo ""
