FROM ubuntu:20.04

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list && \
    apt update && \
    apt install -y software-properties-common && \
    add-apt-repository -y cloud-archive:yoga && \
    apt install -y neutron-linuxbridge-agent=2:20.2.0-0ubuntu1~cloud0 nova-compute=3:25.0.1-0ubuntu1~cloud0 nova-conductor=3:25.0.1-0ubuntu1~cloud0 python3-pip \
                    qemu qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager
RUN pip install python-openstackclient

COPY config-neutron.py /usr/local/bin/config-neutron.py
COPY config-ml2_linuxbridge_agent.py /usr/local/bin/config-ml2_linuxbridge_agent.py
COPY config-nova-compute.py /usr/local/bin/config-nova-compute.py
COPY config-nova.py /usr/local/bin/config-nova.py

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD [ "nova-compute", "--config-file=/etc/nova/nova-compute.conf" ]
