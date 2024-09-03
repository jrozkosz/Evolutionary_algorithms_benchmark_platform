# 1. KVM set up
## Firecracker requires read/write access to /dev/kvm exposed by the KVM module.

## The presence of the KVM module can be checked with:

lsmod | grep kvm

## An example output where it is enabled:

kvm_intel             348160  0 <br />
kvm                   970752  1 kvm_intel <br />
irqbypass              16384  1 kvm <br />

### if it does not display anything you can try:
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils <br />
sudo modprobe kvm <br />
sudo modprobe kvm_intel   # for Intel <br />
sudo modprobe kvm_amd     # for AMD <br />

## Some Linux distributions use the kvm group to manage access to /dev/kvm, while others rely on access control lists. If you have the ACL package for your distro installed, you can grant Read+Write access with:

sudo setfacl -m u:${USER}:rw /dev/kvm

## Otherwise, if access is managed via the kvm group:

[ $(stat -c "%G" /dev/kvm) = kvm ] && sudo usermod -aG kvm ${USER} \
&& echo "Access granted."

# 2. Giving execution rights to all the scripts
chmod +x *.sh

# 3. Getting a Firecracker, rootfs and Guest Kernel Image
sudo apt install -y curl
./install_firecracker_and_ubuntu.sh


### Now it is ready and microVM can be successfully launched by backend server BUT
each microVM has to have a network configured <br />
to define iptables rules host interface has to be given <br />
in setup_network.sh please modify HOST_IFACE to match the one you are using <br />
you can display your available interfaces by typing 'ip link show' <br />
if you are using WIFI the interface name you should use will probably start with 'wl...' <br />
if Ethernet - the name will probably start with 'eth...' <br />
