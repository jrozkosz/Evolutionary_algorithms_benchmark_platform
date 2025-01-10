#!/bin/bash

# author: Jakub Rozkosz

if [ "$#" -ne 2 ];then
  echo "Usage: $0 <VM_IP> <GATEWAY_IP>"
  exit 1
fi

VM_IP=$1
GATEWAY_IP=$2

# Set IP addr and default route
ip addr add $VM_IP/30 dev eth0
ip route add default via $GATEWAY_IP dev eth0

echo "New network configuration:"
ip addr show
ip route show