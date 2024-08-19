#!/bin/bash

# Sprawdzenie, czy podano wszystkie argumenty
if [ "$#" -ne 2 ];then
  echo "Usage: $0 <VM_IP> <GATEWAY_IP>"
  exit 1
fi

VM_IP=$1
GATEWAY_IP=$2

# Debugowanie: Pokaż istniejące interfejsy sieciowe i ich adresy
echo "Debugging network interfaces and routes:"
ip addr show
ip route show

# Czekaj 3 sekund, aby upewnić się, że interfejs sieciowy jest gotowy
sleep 5

# Ustaw adres IP i trasę domyślną
ip addr add $VM_IP/30 dev eth0
ip route add default via $GATEWAY_IP dev eth0

# Debugowanie: Pokaż nową konfigurację sieci
echo "New network configuration:"
ip addr show
ip route show

# Skonfiguruj DNS
echo 'nameserver 8.8.8.8' > /etc/resolv.conf

# mkdir var/lib/dpkg
# touch var/lib/dpkg/status

# Dodaj biblioteki
# Install required packages from local .deb files
# dpkg -i /root/packages/*.deb

# Extract numpy packages (if using tar.gz)
# tar -xzvf /root/numpy-packages.tar.gz -C /root

# Install numpy from the local directory
# pip3 install --no-index --find-links=/root/packages numpy



# echo "Attempting to update package list..."
# apt-get update #|| { echo "apt-get update failed"; exit 1; }

# echo "Installing pip..."
# apt-get install python3-pip -y #|| { echo "pip installation failed"; exit 1; }

echo "Verifying pip installation..."
# pip3 --version #|| { echo "pip is not installed"; exit 1; }
# pip3 list

# echo "Installing numpy..."
# pip3 install numpy #|| { echo "numpy installation failed"; exit 1; }



# Rozpakowanie i instalacja pip z pakietów lokalnych
# cd /root
# tar -xzvf packages.tar.gz
# dpkg -i *.deb

# # Rozpakowanie pakietów numpy
# tar -xzvf numpy-packages.tar.gz -C /root

# # Instalacja numpy z lokalnych źródeł
# pip3 install --no-index --find-links=/root/packages numpy

# # Potwierdzenie instalacji
# pip3 --version
# python3 -c "import numpy; print(numpy.__version__)"


# # Uruchom SSHD
# /usr/sbin/sshd -D