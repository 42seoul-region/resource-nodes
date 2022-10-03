#!/usr/bin/env bash

# Script Path
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
echo "ScriptPath: $SCRIPTPATH"

# Install Neutron, Nova Packages
echo "Install Packages"
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y cloud-archive:yoga
sudo apt install -y neutron-linuxbridge-agent=2:20.2.0-0ubuntu1~cloud0 nova-compute=3:25.0.1-0ubuntu1~cloud0 python3-pip

# Install KVM, QEMU, libvirt
echo "Install libvirt, KVM, QEMU"
$SCRIPTPATH/kvm.sh install

# Install pip and OpenStack client
echo "Install OpenStack Client"
pip install python-openstackclient

# Settings
echo "Settings Neutron"
eval $(cat $SCRIPTPATH/.env) sudo -E $SCRIPTPATH/config-neutron.py

echo "Settings Nova"
eval $(cat $SCRIPTPATH/.env) sudo -E $SCRIPTPATH/config-nova.py

echo "Settings Nova-Compute"
eval $(cat $SCRIPTPATH/.env) sudo -E $SCRIPTPATH/config-nova-compute.py

echo "Starting Services"
sudo systemctl restart nova-compute
sudo systemctl enable nova-compute
sudo systemctl restart neutron-linuxbridge-agent
sudo systemctl enable neutron-linuxbridge-agent
