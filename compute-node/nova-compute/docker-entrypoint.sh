#!/usr/bin/env bash

configure() {
  echo "First configurating Nova-Compute"

  echo "configure neutron.conf..."
  export PROVIDER_INTERFACE_NAME=$(ip -o -4 route show to default | awk '{print $5}')
  export HOST_VLAN_LOCAL=$(ip addr show dev vnet0 | grep inet | awk '{print $2}' | awk -F'/' '{print $1}' | head -n 1)

  echo $PROVIDER_INTERFACE_NAME
  echo $HOST_VLAN_LOCAL

  echo "configure neutron"
  config-neutron.py

  echo "configure linuxbridge_agent.ini..."
  config-ml2_linuxbridge_agent.py

  echo "configure nova.conf..."
  config-nova.py

  echo "configure nova-compute.conf..."
  NOVA_KVM_ACCELERATION=$(egrep -c '(vmx|svm)' /proc/cpuinfo) config-nova-compute.py

  # echo "add cell $CELL_NAME..."
  # echo nova-manage cell_v2 create_cell \
  #   --name $CELL_NAME \
  #   --database_connection  "mysql+pymysql://$MARIADB_USER:$MARIADB_PASSWORD@$HOST_VLAN_LOCAL/$MARIADB_DATABASE?charset=utf8" \
  #   --transport-url "rabbit://$RABBITMQ_DEFAULT_USER:$RABBITMQ_DEFAULT_PASS@$HOST_VLAN_LOCAL:5672/"
  # nova-manage cell_v2 create_cell \
  #   --name $CELL_NAME \
  #   --database_connection  "mysql+pymysql://$MARIADB_USER:$MARIADB_PASSWORD@$HOST_VLAN_LOCAL/$MARIADB_DATABASE?charset=utf8" \
  #   --transport-url "rabbit://$RABBITMQ_DEFAULT_USER:$RABBITMQ_DEFAULT_PASS@$HOST_VLAN_LOCAL:5672/"
  nova-manage db sync
  # adduser $(whoami) libvirt
  # adduser $(whoami) kvm

  rm -rf .env

  echo "done!"
  touch /root/.nova_configured
}

if [ ! -f /root/.nova_configured ]; then
  configure
fi

# /usr/sbin/libvirtd &
# PID_LIBVIRTD=$!

neutron-linuxbridge-agent --config-file=/etc/neutron/plugins/ml2/linuxbridge_agent.ini &
PID_NEUTRON=$!

nova-conductor &
PID_NOVA_CONDUCTOR=$!

"$@" &
PID_MAIN=$!

trap "service_down; exit" SIGTERM

function service_down() {
  echo "Terminating services..."
  # kill -TERM $PID_LIBVIRTD
  kill -TERM $PID_NEUTRON
  kill -TERM $PID_NOVA_CONDUCTOR
  kill -TERM $PID_MAIN
}

# wait $PID_LIBVIRTD
wait $PID_NEUTRON
wait $PID_NOVA_CONDUCTOR
wait $PID_MAIN
