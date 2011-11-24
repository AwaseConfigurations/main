# Copyright 2011 Armens Movsesjans movsesjans@gmail.com
# License: GNU General Public License, version 2 or later
# for AwaseConfigurations Project 
# http://awaseconfigurations.wordpress.com/
# https://github.com/AwaseConfigurations/main
# RR 1

# Add system to server preseed

i=1
for mac in 78:ac:c0:c1:09:e8;
do
sudo cobbler system add --name=host$i --profile=ubuntu-server-i386 --mac=$mac --hostname=host$((i++))
done
