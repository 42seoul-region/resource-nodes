#!/usr/bin/env python3

import os
import configparser

config = configparser.ConfigParser()
config.read('/etc/neutron/neutron.conf')

config['DEFAULT']['transport_url'] = 'rabbit://openstack:{RABBIT_PASS}@{HOST_RABBITMQ}:5672/'.format(**os.environ)

config['keystone_authtoken']['www_authenticate_uri'] = os.environ['KEYSTONE_PUBLIC_ENDPOINT']
config['keystone_authtoken']['auth_url'] = os.environ['KEYSTONE_INTERNAL_ENDPOINT']
config['keystone_authtoken']['memcached_servers'] = '{HOST_VLAN_CONTROLLER}:11211'.format(**os.environ)
config['keystone_authtoken']['auth_type'] = 'password'
config['keystone_authtoken']['project_domain_name'] = 'Default'
config['keystone_authtoken']['user_domain_name'] = 'Default'
config['keystone_authtoken']['project_name'] = 'service'
config['keystone_authtoken']['username'] = os.environ['NEUTRON_USER']
config['keystone_authtoken']['password'] = os.environ['NEUTRON_PASS']

config['oslo_concurrency']['lock_path'] = '/var/lib/neutron/tmp'

with open('/etc/neutron/neutron.conf', 'w') as f1:
    config.write(f1)
