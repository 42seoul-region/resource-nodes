#!/usr/bin/env python3

import os
import configparser

config = configparser.ConfigParser()
config.read('/etc/neutron/plugins/ml2/linuxbridge_agent.ini')

config['DEFAULT']['transport_url'] = 'rabbit://{CONTROLLER_RABBITMQ_USER}:{CONTROLLER_RABBITMQ_PASS}@{HOST_VLAN_CONTROLLER}:5672/'.format(**os.environ)

if 'keystone_authtoken' not in config:
    config['keystone_authtoken'] = {}
config['keystone_authtoken']['www_authenticate_uri'] = os.environ['KEYSTONE_PUBLIC_ENDPOINT']
config['keystone_authtoken']['auth_url'] = os.environ['KEYSTONE_INTERNAL_ENDPOINT']
config['keystone_authtoken']['memcached_servers'] = '{HOST_VLAN_CONTROLLER}:11211'.format(**os.environ)
config['keystone_authtoken']['auth_type'] = 'password'
config['keystone_authtoken']['project_domain_name'] = 'Default'
config['keystone_authtoken']['user_domain_name'] = 'Default'
config['keystone_authtoken']['project_name'] = 'service'
config['keystone_authtoken']['username'] = os.environ['NEUTRON_USER']
config['keystone_authtoken']['password'] = os.environ['NEUTRON_PASS']

if 'oslo_concurrency' not in config:
    config['oslo_concurrency'] = {}
config['oslo_concurrency']['lock_path'] = '/var/lib/neutron/tmp'

with open('/etc/neutron/plugins/ml2/linuxbridge_agent.ini', 'w') as f1:
    config.write(f1)
