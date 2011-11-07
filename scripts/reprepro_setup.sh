#!/bin/bash

# Script for setting up reprepro repository

#sudo apt-get update
#sudo apt-get -y install reprepro
mkdir -p public_html/conf
echo Origin: Awase > public_html/conf/distributions
echo Codename: natty > public_html/conf/distributions
echo Label: Awase-All >> public_html/conf/distributions
echo Suite: stable >> public_html/conf/distributions
echo Version: 0.1 >> public_html/conf/distributions
echo Architectures: i386 amd64 source >> public_html/conf/distributions
echo Components: main non-free contrib >> public_html/conf/distributions
echo Description: AwaseConfigurations >> public_html/conf/distributions
