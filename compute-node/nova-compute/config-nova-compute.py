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

config['DEFAULT']['transport_url'] = 'rabbit://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{HOST_VLAN_LOCAL}:5672/'.format(**os.environ)
config['DEFAULT']['my_ip'] = os.environ['HOST_VLAN_LOCAL']
config['DEFAULT']['instances_path'] = '/var/lib/nova/instances'

if 'keystone_authtoken' not in config:
    config['keystone_authtoken'] = {}
config['keystone_authtoken']['www_authenticate_uri'] = os.environ['KEYSTONE_PUBLIC_ENDPOINT']
config['keystone_authtoken']['auth_url'] = os.environ['KEYSTONE_INTERNAL_ENDPOINT']
config['keystone_authtoken']['memcached_servers'] = '{HOST_VLAN_CONTROLLER}:11211'.format(**os.environ)
config['keystone_authtoken']['auth_type'] = 'password'
config['keystone_authtoken']['project_domain_name'] = 'Default'
config['keystone_authtoken']['user_domain_name'] = 'Default'
config['keystone_authtoken']['project_name'] = 'service'
config['keystone_authtoken']['username'] = os.environ['NOVA_USER']
config['keystone_authtoken']['password'] = os.environ['NOVA_PASS']

if 'placement' not in config:
    config['placement'] = {}
config['placement']['region_name'] = os.environ['REGION_ID']
config['placement']['project_domain_name'] = 'Default'
config['placement']['project_name'] = 'service'
config['placement']['auth_type'] = 'password'
config['placement']['user_domain_name'] = 'Default'
config['placement']['auth_url'] = 'http://{HOST_VLAN_CONTROLLER}:5000/v3'.format(**os.environ)
config['placement']['username'] = os.environ['PLACEMENT_API_USER']
config['placement']['password'] = os.environ['PLACEMENT_API_PASS']

with open('/etc/nova/nova-compute.conf', 'w') as f1:
    config.write(f1)
