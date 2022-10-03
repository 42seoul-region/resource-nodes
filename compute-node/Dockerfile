FROM ubuntu:20.04

RUN apt update && \
    apt install -y software-properties-common && \
    add-apt-repository -y cloud-archive:yoga && \
    apt install -y neutron-linuxbridge-agent=2:20.2.0-0ubuntu1~cloud0 nova-compute=3:25.0.1-0ubuntu1~cloud0 python3-pip \
                    qemu qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager
RUN pip install python-openstackclient

COPY config-neutron.py /usr/local/bin/config-neutron.py
COPY config-nova-compute.py /usr/local/bin/config-nova-compute.py
COPY config-nova.py /usr/local/bin/config-nova.py
COPY .env .

RUN eval $(cat .env) config-neutron.py
RUN eval $(cat .env) config-nova.py
RUN eval $(cat .env) config-nova-compute.py

# entry: /usr/sbin/libvirtd

# sudo systemctl restart nova-compute
# sudo systemctl enable nova-compute
# sudo systemctl restart neutron-linuxbridge-agent
# sudo systemctl enable neutron-linuxbridge-agent

# nova-manage cell_v2 create_cell \
#     --name cell1 \
#     --database_connection  mysql+pymysql://root:secretmysql@127.0.0.1/nova?charset=utf8 \
#     --transport-url rabbit://stackrabbit:secretrabbit@mqserver:5672/
