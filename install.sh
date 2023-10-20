#!/bin/bash

INSTALL_LOC='/opt/copycat'
ALIAS='alias copycat="'${INSTALL_LOC}'/.venv/bin/python3 '${INSTALL_LOC}'/__main__.py"'

echo "SUDO required for install"
sudo mkdir -p $INSTALL_LOC/img
sudo cp -r * $INSTALL_LOC
sudo python3 -m venv $INSTALL_LOC/.venv
sudo $INSTALL_LOC/.venv/bin/python3 -m pip install -r $INSTALL_LOC/requirements.txt
sudo chown -R $USER:$USER $INSTALL_LOC

echo 'Python environment installation succeeded.'

sudo rm ${INSTALL_LOC}/requirements.txt ${INSTALL_LOC}/install.sh

if ! grep -Fxq "$ALIAS" ~/.bashrc
then
echo  $ALIAS >> ~/.bashrc
fi

source ~/.bashrc

echo 'Copycat installation succeeded.'
echo 'To launch app, simply type: copycat'

${INSTALL_LOC}/.venv/bin/python3 ${INSTALL_LOC}/__main__.py
