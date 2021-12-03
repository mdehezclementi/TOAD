#!/bin/bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

npm init

npm install truffle
npm install ganache-cli

snap install ipfs

ipfs init
