#!/bin/bash

host="127.0.0.1"
port="22"
user="pointname"
tmpdir="/tmp/iissh"
offlineFetch="./ii-db-utils/offline-fetch.py"
echoareas="test.15"

tossesdir_remote="/home/$user/tosses/"
destdir_remote="/srv/iissh/"
tossesdir="./tosses/"
destdir="./base/"

printhelp() {
	echo "Usage: iissh.sh [ fetch | send ]"
}
connect() {
	mkdir -p $tmpdir
	sshfs -p $port $user@$host:/ $tmpdir
	
	if [ $? -ne 0 ]; then
		echo "Ошибка подключения"
		exit 1
	fi
}
disconnect() {
	fusermount -u $tmpdir
}

fetch() {
	connect
	echo "$echoareas" | $offlineFetch $tmpdir/$destdir_remote $destdir
	disconnect
}
send() {
	connect
	tosses=`find $tossesdir -maxdepth 1 -type f -name "*.toss" | sort -g`
	for toss in ${tosses[*]}; do
		cp $toss $tmpdir/$tossesdir_remote
		bname=`basename $toss .toss`
		mv $toss $tossesdir/$bname.out
	done
	disconnect
}

case $1 in
fetch) fetch;;
send) send;;
*) printhelp;;
esac
