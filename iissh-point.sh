#!/bin/bash

if [ "$1" == "" ]; then
	echo "Usage: iissh-point.sh pointname"
	exit 1
fi

useradd -m -c "$1" -s /usr/lib/openssh/sftp-server $1
usermod -a -G $1 iissh
usermod -a -G iissh $1
passwd $1

mkdir -p /home/$1/tosses

chown iissh:$1 /home/$1/*
chmod 775 /home/$1/tosses
