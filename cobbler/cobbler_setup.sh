mkdir ~/cobbler_wgets
cd ~/cobbler_wgets

wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/settings
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/interfaces
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/dhcp.template
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/cobbler_add_systems.sh
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/cobbler_remove_systems.sh
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/ubuntu-nqa.seed
wget https://raw.github.com/AwaseConfigurations/main/master/cobbler/wakeup.sh
wget http://releases.ubuntu.com/natty/ubuntu-11.04-alternate-i386.iso

sudo software-properties-gtk -e universe
sudo apt-get install dhcp3-server cobbler cobbler-common wakeonlan

sudo service cobbler start
sleep 1
sudo cobbler check

sudo cp interfaces /etc/network/
sudo /etc/init.d/networking restart
sudo cp settings /etc/cobbler/
sudo cp dhcp.template /etc/cobbler/
sudo cp ubuntu-nqa.seed /var/lib/cobbler/kickstarts/

sudo service cobbler restart
sleep 1
sudo cobbler sync

sudo mount -o loop ubuntu-11.04-alternate-i386.iso /mnt
sudo cobbler import --name=ubuntu-alternate --path=/mnt --breed=ubuntu
sudo cobbler profile edit --name=ubuntu-alternate-i386 --kickstart=/var/lib/cobbler/kickstarts/ubuntu-nqa.seed --kopts="priority=critical locale=en_US"

sudo service cobbler restart
sleep 1
sudo cobbler sync

chmod 700 cobbler_add_systems.sh
./cobbler_add_systems.sh

sudo service cobbler restart
sleep 1
sudo cobbler sync

chmod 700 wakeup.sh
./wakeup.sh

