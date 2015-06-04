#!/bin/bash

mkdir -p /srv/iissh/
useradd -d /srv/iissh -c "bot for ii-ssh" -U iissh

mkdir -p /srv/iissh/echo /srv/iissh/msg
chown -R iissh:iissh /srv/iissh/
