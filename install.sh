#!/bin/bash

INSTALL_LOC='/opt/copycat'

echo "SUDO required for install"
sudo apt install python3-venv -y
sudo mkdir -p $INSTALL_LOC/{tmp,img}
sudo cp -r * $INSTALL_LOC
sudo python3 -m venv $INSTALL_LOC/.venv
sudo $INSTALL_LOC/.venv/bin/python3 -m pip install -r $INSTALL_LOC/requirements.txt
sudo chown -R $USER:$USER $INSTALL_LOC

echo 'Python installation succeeded.'

cd ..
python3 copycat
