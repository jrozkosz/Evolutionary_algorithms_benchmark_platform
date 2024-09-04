#!/bin/bash

# author: Jakub Rozkosz

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <tap_device> <tap_ip>"
    exit 1
fi

TAP_DEV="$1"
TAP_IP="$2"
MASK_SHORT="/30"

sudo ip link del "$TAP_DEV" 2> /dev/null || true
sudo ip tuntap add dev "$TAP_DEV" mode tap
sudo ip addr add "${TAP_IP}${MASK_SHORT}" dev "$TAP_DEV"
sudo ip link set dev "$TAP_DEV" up


HOST_IFACE="wlp2s0"

sudo iptables -D FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT || true
sudo iptables -D FORWARD -i "$TAP_DEV" -o "$HOST_IFACE" -j ACCEPT || true
sudo iptables -D FORWARD -i "$HOST_IFACE" -o "$TAP_DEV" -j ACCEPT || true

sudo iptables -I FORWARD 1 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 1 -i "$TAP_DEV" -o "$HOST_IFACE" -j ACCEPT
sudo iptables -I FORWARD 1 -i "$HOST_IFACE" -o "$TAP_DEV" -j ACCEPT