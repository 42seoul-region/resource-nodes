#!/usr/bin/env bash

self=$0
command=$1

if [ ! $command ]; then
    echo "type command"
    exit 1
fi

if [ $command = 'install' ]; then
    echo "Updating packages"
    sudo apt update

    # Mandatory Packages
    # from: https://ubuntu.com/blog/kvm-hyphervisor
    echo "installing kvm, qemu"
    sudo apt install -y qemu qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
    # Install a service
    sudo systemctl enable libvirtd --now

    # Manager
    # from: https://virt-manager.org/
    echo "installing virt-manager"
    sudo apt install -y virt-manager
    # Usage: run sudo virt-manager

    # add me to kvm group?
    # read -p 'add me to libvirt and kvm group? (y/n): ' ANSWER
    # if [ $ANSWER = 'y' ]; then
        $self adduser
    # fi
elif [ $command = 'adduser' ]; then
    username=$2
    if [ ! $username ]; then
        username=$(whoami)
    fi
    sudo adduser $username libvirt
    sudo adduser $username kvm
elif [ $command = 'check' ]; then
    echo "vmx or svm capable: $(egrep -c '(vmx|svm)' /proc/cpuinfo)"
    echo "checking kvm-ok"
    kvm-ok
    if [ $? -ne 127 ]; then
        echo "trying install cpu-checker.."
        sudo apt install cpu-checker
    fi
    sudo kvm-ok
else
    echo "unknown command $command"
fi
