#!/bin/bash

# Script for setting static IP address. Run with sudo.

echo auto lo > interfaces.static
echo iface lo inet loopback >> interfaces.static
echo >> interfaces.static
echo auto eth0 >> interfaces.static
echo iface eth0 inet static >> interfaces.static
echo -n -e address\ >> interfaces.static
hostname -I >> interfaces.static
echo netmask 255.255.0.0 >> interfaces.static
echo network 172.28.0.0 >> interfaces.static
echo broadcast 172.28.255.255 >> interfaces.static
echo gateway 172.28.1.254 >> interfaces.static
cat /etc/network/interfaces > /etc/network/interfaces.old
cat interfaces.static > /etc/network/interfaces
rm interfaces.static
/etc/init.d/networking restart

