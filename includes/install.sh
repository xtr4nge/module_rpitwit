#!/bin/bash

echo "installing python-setuptools..."
apt-get install python-setuptools

echo "installing RPItwit..."
easy_install twitter
easy_install rpitwit

echo "..DONE.."
exit
