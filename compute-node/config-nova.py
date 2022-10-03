#!/usr/bin/env python3

import os
import configparser

config = configparser.ConfigParser()
config.read('/etc/nova/nova.conf')

config['DEFAULT']['transport_url'] = 'rabbit://openstack:{RABBIT_PASS}@{HOST_RABBITMQ}:5672/'.format(**os.environ)
config['DEFAULT']['my_ip'] = os.environ['HOST_VLAN_LOCAL']

config['keystone_authtoken']['www_authenticate_uri'] = os.environ['KEYSTONE_PUBLIC_ENDPOINT']
config['keystone_authtoken']['auth_url'] = os.environ['KEYSTONE_INTERNAL_ENDPOINT']
config['keystone_authtoken']['memcached_servers'] = '{HOST_VLAN_CONTROLLER}:11211'.format(**os.environ)
config['keystone_authtoken']['auth_type'] = 'password'
config['keystone_authtoken']['project_domain_name'] = 'Default'
config['keystone_authtoken']['user_domain_name'] = 'Default'
config['keystone_authtoken']['project_name'] = 'service'
config['keystone_authtoken']['username'] = os.environ['NOVA_USER']
config['keystone_authtoken']['password'] = os.environ['NOVA_PASS']

config['vnc']['enabled'] = 'true'
config['vnc']['server_listen'] = '0.0.0.0'
config['vnc']['server_proxyclient_address'] = os.environ['HOST_VLAN_LOCAL']
config['vnc']['novncproxy_base_url'] = 'http://{HOST_VLAN_CONTROLLER}:6080/vnc_auto.html'.format(**os.environ)

config['glance']['api_servers'] = 'http://{HOST_VLAN_CONTROLLER}:9292'.format(**os.environ)

config['neutron']['auth_url'] = os.environ['KEYSTONE_INTERNAL_ENDPOINT']
config['neutron']['auth_type'] = 'password'
config['neutron']['project_domain_name'] = 'default'
config['neutron']['user_domain_name'] = 'default'
config['neutron']['project_name'] = 'service'
config['neutron']['region_name'] = os.environ['REGION_ID']
config['neutron']['username'] = os.environ['NEUTRON_USER']
config['neutron']['password'] = os.environ['NEUTRON_PASS']

config['placement']['region_name'] = os.environ['REGION_ID']
config['placement']['project_domain_name'] = 'Default'
config['placement']['project_name'] = 'service'
config['placement']['auth_type'] = 'password'
config['placement']['user_domain_name'] = 'Default'
config['placement']['auth_url'] = 'http://{HOST_VLAN_CONTROLLER}:5000/v3'.format(**os.environ)
config['placement']['username'] = os.environ['PLACEMENT_API_USER']
config['placement']['password'] = os.environ['PLACEMENT_API_PASS']

config['oslo_concurrency']['lock_path'] = '/var/lib/nova/tmp'

with open('/etc/nova/nova.conf', 'w') as f1:
    config.write(f1)
