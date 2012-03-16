#!/bin/bash

# This script will automatically upgrade Ubuntu 11.04 to Ubuntu 11.10
#
# Copyright 2011 Henri Siponen
# License: GNU General Public License, version 2 or later

sudo /etc/init.d/puppet stop
sudo sed -i 's/natty/oneiric/g' /etc/apt/sources.list
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get dist-upgrade -o Dpkg::Options::="--force-confold" --force-yes -y
sudo reboot

