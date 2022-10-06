#!/usr/bin/env bash

configure() {
  echo "First configurating Nova-Compute"

  echo "configure neutron.conf..."
  export PROVIDER_INTERFACE_NAME=$(ip -o -4 route show to default | awk '{print $5}')
  eval $(cat .env) ./config-neutron.py

  echo "configure linuxbridge_agent.ini..."
  eval $(cat .env) ./config-ml2_linuxbridge_agent.py

  echo "configure nova.conf..."
  eval $(cat .env) ./config-nova.py

  echo "configure nova-compute.conf..."
  eval $(cat .env) ./config-nova-compute.py

  echo "add cell $CELL_NAME..."
  nova-manage cell_v2 create_cell \
    --name $CELL_NAME \
    --database_connection  mysql+pymysql://$MARIADB_USER:$MARIADB_PASSWORD@$HOST_VLAN_LOCAL/$MARIADB_DATABASE?charset=utf8 \
    --transport-url rabbit://openstack:$RABBIT_PASS@$HOST_RABBITMQ:5672/

  # adduser $(whoami) libvirt
  # adduser $(whoami) kvm

  rm -rf .env

  echo "done!"
  touch /root/.nova_configured
}

if [ ! -f /root/.nova_configured ]; then
  configure
fi

/usr/sbin/libvirtd &
PID_LIBVIRTD=$!

neutron-linuxbridge-agent --config-file=/etc/neutron/plugins/ml2/linuxbridge_agent.ini &
PID_NEUTRON=$!

trap "service_down; exit" SIGTERM

function service_down() {
  echo "Terminating services..."
  kill -TERM $PID_LIBVIRTD
  kill -TERM $PID_NEUTRON
}

exec "$@"
