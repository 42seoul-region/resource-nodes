#!/usr/bin/env python3

import os
import configparser

config = configparser.ConfigParser()
config.read('/etc/nova/nova-compute.conf')

kvm_accel = int(os.environ['NOVA_KVM_ACCELERATION'])
if (kvm_accel > 0):
    config['libvirt']['virt_type'] = 'kvm'
    print('Activated KVM acceleration')
else:
    config['libvirt']['virt_type'] = 'qemu'
    print('Not activated KVM acceleration')

with open('/etc/nova/nova-compute.conf', 'w') as f1:
    config.write(f1)
