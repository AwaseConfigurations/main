# Copyright 2011 Armens Movsesjans movsesjans@gmail.com
# License: GNU General Public License, version 2 or later
# for AwaseConfigurations Project 
# http://awaseconfigurations.wordpress.com/
# https://github.com/AwaseConfigurations/main
# RR 1

# Add systems to the alternate preseed

i=2
for mac in 78:ac:c0:ba:79:73 78:ac:c0:c0:8a:e4 78:ac:c0:c0:88:53 78:ac:c0:c1:1b:80 78:ac:c0:c2:8c:5e 78:ac:c0:c0:88:79 78:ac:c0:c1:09:a3 78:ac:c0:c1:05:f4 78:ac:c0:c0:8b:47 78:ac:c0:c2:8c:83 78:ac:c0:c4:09:17 78:ac:c0:c2:8c:5a 78:ac:c0:c2:8c:85 78:ac:c0:c0:8a:8b 78:ac:c0:c0:8f:9b 78:ac:c0:c1:0a:96 78:ac:c0:c4:09:18 78:ac:c0:c4:09:1c 2c:41:38:b5:f2:6b 78:ac:c0:c2:8b:62 2c:27:d7:19:01:3e 78:ac:c0:c0:89:f5 78:ac:c0:c0:88:93 78:ac:c0:c0:8e:47;
do
  sudo cobbler system add --name=host$i --profile=ubuntu-alternate-i386 --mac=$mac --hostname=host$((i++))
done
