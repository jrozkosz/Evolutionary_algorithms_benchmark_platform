#!/bin/bash

# Define the paths
VENV_DIR="microVM_venv"

# Create a Python virtual environment and install necessary libraries
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install numpy
deactivate

# Define the new shebang line
NEW_SHEBANG="#!/root/microVM_venv/bin/python3"

# List of files in which shebang line need to be altered
FILES_TO_UPDATE=("$VENV_DIR/bin/pip" "$VENV_DIR/bin/pip3" "$VENV_DIR/bin/pip3.10")

# Loop through each file and update the shebang
for FILE in "${FILES_TO_UPDATE[@]}"; do
    if [ -f "$FILE" ]; then
        echo "Updating shebang in $FILE"
        sudo sed -i "1s|.*|$NEW_SHEBANG|" "$FILE"
    else
        echo "$FILE not found, skipping..."
    fi
done

ROOTFS="ubuntu-22.04.ext4"

# Mount the rootfs image
echo "Mounting the rootfs image..."
sudo mkdir -p /mnt/vm_root
if ! sudo mount -o loop $ROOTFS /mnt/vm_root; then
    echo "Failed to mount $ROOTFS"
    exit 1
fi

# Copy the init_setup.sh script and the python script to the rootfs
echo "Copying python virtual environment to the rootfs..."
if ! sudo cp -r "$VENV_DIR"/ /mnt/vm_root/root; then
    echo "Failed to copy venv..."
    sudo umount /mnt/vm_root
    exit 1
fi

# Unmount the rootfs image
echo "Unmounting the rootfs image..."
if ! sudo umount /mnt/vm_root; then
    echo "Failed to unmount /mnt/vm_root"
    exit 1
fi

echo "Rootfs image updated with Python virtual environment and numpy installed."
