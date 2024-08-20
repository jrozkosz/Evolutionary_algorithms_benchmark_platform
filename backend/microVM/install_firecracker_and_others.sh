# Downloading a rootfs and guest kernel image
ARCH="$(uname -m)"

latest=$(wget "http://spec.ccfc.min.s3.amazonaws.com/?prefix=firecracker-ci/v1.9/x86_64/vmlinux-5.10&list-type=2" -O - 2>/dev/null | grep "(?<=<Key>)(firecracker-ci/v1.9/x86_64/vmlinux-5\.10\.[0-9]{3})(?=</Key>)" -o -P)

## Download a linux kernel binary
wget https://s3.amazonaws.com/spec.ccfc.min/${latest} -O vmlinux

## Download a rootfs
wget https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.9/${ARCH}/ubuntu-22.04.ext4

## Download the ssh key for the rootfs
wget https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.9/${ARCH}/ubuntu-22.04.id_rsa

## Set user read permission on the ssh key
chmod 400 ./ubuntu-22.04.id_rsa

## Resize the rootfs memory
sudo ./resize_rfs_memory.sh

## Install in the rootfs python virtual environment with all the necessary libraries
sudo ./resize_rootfs.sh

# Getting a Firecracker Binary
ARCH="$(uname -m)"
release_url="https://github.com/firecracker-microvm/firecracker/releases"
latest=$(basename $(curl -fsSLI -o /dev/null -w  %{url_effective} ${release_url}/latest))
curl -L ${release_url}/download/${latest}/firecracker-${latest}-${ARCH}.tgz \
| tar -xz

## Rename the binary to "firecracker"
mv release-${latest}-$(uname -m)/firecracker-${latest}-${ARCH} firecracker