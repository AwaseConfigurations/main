#!/bin/bash

# This script will automatically upgrade Ubuntu 11.04 to Ubuntu 11.10
#
# Copyright 2011 Henri Siponen
# License: GNU General Public License, version 2 or later

wget https://github.com/AwaseConfigurations/main/raw/master/packages/apt/oneiric-sources/oneiric-sources_0.1_all.deb
sudo apt-get -y install gdebi
sudo gdebi -n oneiric-sources_0.1_all.deb
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
sudo apt-get -y remove oneiric-sources
sudo cp /etc/apt/sources.list.backup /etc/apt/sources.list
sudo rm /etc/apt/sources.list.backup
sudo rm /etc/apt/sources.list.hng
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get dist-upgrade -o Dpkg::Options::="--force-confold" --force-yes -y
sudo reboot

