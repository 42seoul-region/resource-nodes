#!/usr/bin/env bash

set -e

# Install Network Utilities
echo "Install network utilities"
sudo apt-get update
sudo apt-get install -y iproute2 net-tools openssh-server bridge-utils vlan
sudo systemctl enable ssh --now

# Kernel Module Setting.
# We cannot modify them in Docker. We need to do it here.
# echo "Modify kernel module setting"
# sudo sysctl -w net.ipv4.conf.default.rp_filter=0
# sudo sysctl -w net.ipv4.conf.all.rp_filter=0
# sudo sysctl net.ipv4.ip_forward=1
# sudo sysctl -p

# UFW Setting
echo "Setting UFW"
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable
