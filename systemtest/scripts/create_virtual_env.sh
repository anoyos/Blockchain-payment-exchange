#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Supply code artifact token: './scripts/create_virtual_env.sh \$token'"
    exit 1
fi

virtualenv -p python3.8 venv
source venv/bin/activate

pip3 config set global.index-url https://aws:$1@pypi-repo-364206529396.d.codeartifact.eu-west-1.amazonaws.com/pypi/pypi-store/simple/
pip3 install -r requirements.txt
