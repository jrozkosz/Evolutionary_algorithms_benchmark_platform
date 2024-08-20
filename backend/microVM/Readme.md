# 1. KVM set up
## Firecracker requires read/write access to /dev/kvm exposed by the KVM module.

## The presence of the KVM module can be checked with:

lsmod | grep kvm

## An example output where it is enabled:

kvm_intel             348160  0
kvm                   970752  1 kvm_intel
irqbypass              16384  1 kvm

## Some Linux distributions use the kvm group to manage access to /dev/kvm, while others rely on access control lists. If you have the ACL package for your distro installed, you can grant Read+Write access with:

sudo setfacl -m u:${USER}:rw /dev/kvm

## Otherwise, if access is managed via the kvm group:

[ $(stat -c "%G" /dev/kvm) = kvm ] && sudo usermod -aG kvm ${USER} \
&& echo "Access granted."

# 3. Giving execution rights to all the scripts
chmod +x *.sh

# Getting a Firecracker, rootfs and Guest Kernel Image
sudo ./install_firecracker_and_others.sh

### Now it is ready and microVM can be successfully launched by backend server BUT
each microVM has to have a network configured
to define iptables rules host interface has to be given
in setup_network.sh please modify HOST_IFACE to match the one you are using
you can display your available interfaces by typing 'ip link show'
if you are using WIFI the interface name you should use will probably start with 'wl...'
if Ethernet - the name will probably start with 'eth...'