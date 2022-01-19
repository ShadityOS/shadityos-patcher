#!/bin/bash

cp patcher.py /usr/bin/shadityos-patcher
chmod +x /usr/bin/shadityos-patcher
apt update
apt upgrade
apt install python3 python3-pip python3-dev python3-wget
pip3 install requests wget

