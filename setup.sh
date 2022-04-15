#! /bin/bash

# Install peerflix

sudo npm -g i peerflix
pip install -r requirements.txt 

sl=$(echo `(which $SHELL)` | awk -F "/" '{print $3}')

echo "alias t-stream='python $(pwd)/src/app.py'" >> ~/.${sl}rc
