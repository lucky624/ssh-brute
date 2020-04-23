#!/bin/bash

virtualenv -p $(which python2.7) venv
source venv/bin/activate
pip install paramiko
pip install colorama

echo -e "\n\n\nPlease run command : \`source venv/bin/activate\`"
