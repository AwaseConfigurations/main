# Copyright 2011 Armens Movsesjans movsesjans@gmail.com
# License: GNU General Public License, version 2 or later
# for AwaseConfigurations Project 
# http://awaseconfigurations.wordpress.com/
# https://github.com/AwaseConfigurations/main

#create a temp folder
mkdir ~/cobbler_wgets
cd ~/cobbler_wgets

#download preconfigured cobbler setup files and scripts from github:awaseconfigurations
#download ubuntu-11.04-alternate-i386.iso
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/settings
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/interfaces
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/dhcp.template
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/cobbler_add_systems.sh
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/cobbler_remove_systems.sh
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/ubuntu-nqa.seed
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/wakeup.sh
wget http://releases.ubuntu.com/natty/ubuntu-11.04-alternate-i386.iso

#enable universe repo and install packages
sudo software-properties-gtk -e universe
sudo apt-get update
sudo apt-get install dhcp3-server cobbler cobbler-common wakeonlan

#start cobbler and build its configuration
sudo service cobbler start
sleep 1
sudo cobbler check

#copy setup files to where they belong
sudo cp interfaces /etc/network/
sudo /etc/init.d/networking restart
sudo cp settings /etc/cobbler/
sudo cp dhcp.template /etc/cobbler/
sudo cp ubuntu-nqa.seed /var/lib/cobbler/kickstarts/

#restart and rebuild cobbler
sudo service cobbler restart
sleep 1
sudo cobbler sync

#mount ubuntu image, ipport it with cobbler, and assign a preconfigured preseed
sudo mount -o loop ubuntu-11.04-alternate-i386.iso /mnt
sudo cobbler import --name=ubuntu-alternate --path=/mnt --breed=ubuntu
sudo cobbler profile edit --name=ubuntu-alternate-i386 --kickstart=/var/lib/cobbler/kickstarts/ubuntu-nqa.seed --kopts="priority=critical locale=en_US"

#restart and rebuild cobbler
sudo service cobbler restart
sleep 1
sudo cobbler sync

#run the script to add systems (machines) to same profile as preseed
#they will then pick this network install by default
chmod 700 cobbler_add_systems.sh
./cobbler_add_systems.sh

#restart and rebuild cobbler
sudo service cobbler restart
sleep 1
sudo cobbler sync

#run the script to wake all up
chmod 700 wakeup.sh
./wakeup.sh
