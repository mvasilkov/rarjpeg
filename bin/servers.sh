#!/bin/bash
memcached -d
screen -d -m postgres -D /usr/local/var/postgres
