#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Supply code artifact token: './scripts/create_virtual_env.sh \$token'"
    exit 1
fi

/usr/local/bin/python -m pip install --upgrade pip
pip3 install virtualenv
virtualenv -p python3.8 venv
source venv/bin/activate
python -m pip install --upgrade pip

pip3 config set global.index-url https://aws:$1@pypi-repo-101351886674.d.codeartifact.eu-west-1.amazonaws.com/pypi/pypi/simple/
pip3 install -r requirements.txt
