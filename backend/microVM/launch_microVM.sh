#!/bin/bash

# author: Jakub Rozkosz

# Check if the arguments are provided
if [ "$#" -ne 10 ]; then
  echo "Usage: $0 <tap_device> <firecracker_socket> <vm_ip> <gateway_ip> <ssh_key> <algorithm_file> <CECfunctions> <algorithm_running> <ranking_params> <algorithm_name>"
  exit 1
fi

TAP_DEVICE=$1
FIRECRACKER_SOCKET=$2
VM_IP=$3
GATEWAY_IP=$4
SSH_KEY=$5
ALGORITHM_FILE=$6
CECFUNCTIONS=$7
ALGORITHM_RUNNING=$8
RANKING_PARAMS=$9
ALGORITHM_NAME="${10}"
# CEC_DATA="${10}"
CONFIG_TEMPLATE="vm_config_template.json"
CONFIG_FILE="vm_config_$(date +%s).json"
ROOTFS="ubuntu-22.04_$(date +%s).ext4"
ORIGINAL_ROOTFS="ubuntu-22.04.ext4"
INIT_SCRIPT="init_setup.sh"

# Print all the arguments
echo "TAP_DEVICE: $TAP_DEVICE"
echo "FIRECRACKER_SOCKET: $FIRECRACKER_SOCKET"
echo "VM_IP: $VM_IP"
echo "GATEWAY_IP: $GATEWAY_IP"
echo "SSH_KEY: $SSH_KEY"
echo "ALGORITHM_FILE: $ALGORITHM_FILE"
echo "CECFUNCTIONS: $CECFUNCTIONS"
echo "ALGORITHM_RUNNING: $ALGORITHM_RUNNING"
echo "ALGORITHM_NAME: $ALGORITHM_NAME"
echo "RANKING_PARAMS: $(basename "$RANKING_PARAMS")"
# echo "CEC_DATA: $CEC_DATA"

# Check if the configuration template file exists
if [ ! -f "$CONFIG_TEMPLATE" ]; then
  echo "Template configuration file not found!"
  exit 1
fi

# Set up the network on host
echo "Setting up the network of microVM on host..."
./setup_network.sh $TAP_DEVICE $GATEWAY_IP

# Create a copy of the original rootfs image
echo "Creating a copy of the original rootfs image..."
cp "$ORIGINAL_ROOTFS" "$ROOTFS"

# Check if the rootfs image exists
if [ ! -f "$ROOTFS" ]; then
  echo "Root filesystem image not found!"
  exit 1
fi

# Generate the configuration file from the template
sed "s/__TAP_DEVICE__/$TAP_DEVICE/; s#__ROOTFS_PATH__#$ROOTFS#" "$CONFIG_TEMPLATE" > "$CONFIG_FILE"

# Mount the rootfs image
echo "Mounting the rootfs image..."
mkdir -p /mnt/vm_root
if ! sudo mount -o loop $ROOTFS /mnt/vm_root; then
    echo "Failed to mount $ROOTFS"
    exit 1
fi

# Remove unnecessary files from rootfs
echo "Removing unnecessary files from rootfs..."
rm -rf /mnt/vm_root/var/cache/apt/archives/*
rm -rf /mnt/vm_root/tmp/*

# Copy the init_setup.sh script and the python script to the rootfs
echo "Copying the init_setup.sh, python scripts and libraries to the rootfs..."
if ! cp "$INIT_SCRIPT" /mnt/vm_root/root/init_setup.sh || ! cp "$ALGORITHM_FILE" /mnt/vm_root/root/$ALGORITHM_FILE || 
   ! cp "$CECFUNCTIONS" /mnt/vm_root/root/$CECFUNCTIONS || ! cp "$ALGORITHM_RUNNING" /mnt/vm_root/root/$ALGORITHM_RUNNING ||
   ! cp -r input_data/ /mnt/vm_root/root || ! ls /mnt/vm_root/root || ! ls /mnt/vm_root/root/input_data || 
   ! cp "$RANKING_PARAMS" /mnt/vm_root/root/$(basename "$RANKING_PARAMS") || ! cp "$SSH_KEY" /mnt/vm_root/root/$SSH_KEY; then
    echo "Failed to copy one or more scripts"
    sudo umount /mnt/vm_root
    exit 1
fi
chmod +x /mnt/vm_root/root/init_setup.sh

# Create the rc.local script to automatically run init_setup.sh
echo "Creating the rc.local script to automatically run init_setup.sh..."
if ! bash -c "cat > /mnt/vm_root/etc/rc.local" <<EOL
#!/bin/sh -e
/root/init_setup.sh $VM_IP $GATEWAY_IP
exit 0
EOL
then
    echo "Failed to create /mnt/vm_root/etc/rc.local"
    sudo umount /mnt/vm_root
    exit 1
fi
chmod +x /mnt/vm_root/etc/rc.local

# Unmount the rootfs image
echo "Unmounting the rootfs image..."
if ! sudo umount /mnt/vm_root; then
    echo "Failed to unmount /mnt/vm_root"
    exit 1
fi

# Remove the algorithm file
rm $ALGORITHM_FILE

# Start Firecracker
echo "Starting Firecracker microVM..."
sudo rm -f $FIRECRACKER_SOCKET
sudo ./firecracker --api-sock "$FIRECRACKER_SOCKET" --config-file "$CONFIG_FILE" &

# Wait for the microVM to boot and configure the network
sleep 3

# Remove the copied rootfs image and configuration file after the microVM has finished its work
echo "Removing the copied rootfs image and configuration file..."
rm -f $ROOTFS
rm -f $CONFIG_FILE

mkdir -p ../running_files

scp_loop() {
    while true; do
        sleep 5
        scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "root@$VM_IP:/root/progress_file_$ALGORITHM_NAME.txt" ../running_files/
    done
}

scp_loop &
SCP_LOOP_PID=$!

# Run user code ranking
echo "Running user's algorithm..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no root@$VM_IP "source microVM_venv/bin/activate && \ 
                /root/microVM_venv/bin/python3 /root/$ALGORITHM_RUNNING "$ALGORITHM_NAME" > running_logs_$ALGORITHM_NAME.txt && \
                deactivate"

RET_CODE=$?
echo "RETURN CODE"
echo $RET_CODE

# wait for the last progress_file.txt update
sleep 6

kill $SCP_LOOP_PID
wait $SCP_LOOP_PID 2>/dev/null

# Copy the results of the ranking from microVM to the host
# if [ $RET_CODE -eq 0 ]; then
scp -i $SSH_KEY -o StrictHostKeyChecking=no root@$VM_IP:/root/running_logs_$ALGORITHM_NAME.txt ../running_files/
scp -i $SSH_KEY -o StrictHostKeyChecking=no root@$VM_IP:/root/running_results_$ALGORITHM_NAME.json ../running_files/
# fi

# Kill the microVM
ssh -i $SSH_KEY -o StrictHostKeyChecking=no root@$VM_IP 'reboot'

sudo rm -f $FIRECRACKER_SOCKET

echo "Removing TAP device $TAP_DEVICE..."
sudo ip link del "$TAP_DEVICE" || true

exit $RET_CODE