#!/bin/bash

# Set the new size for the image
NEW_SIZE="1G"
IMAGE_NAME="ubuntu-22.04.ext4"

# Resize the disk image
echo "Resizing disk image to $NEW_SIZE..."
qemu-img resize $IMAGE_NAME $NEW_SIZE

# Verify the new size
echo "Verifying new image size..."
qemu-img info $IMAGE_NAME

# Mount the new image
MOUNT_DIR="/mnt/new"
echo "Creating mount directory..."
sudo mkdir -p $MOUNT_DIR

echo "Mounting the new image..."
sudo mount -o loop $IMAGE_NAME $MOUNT_DIR

# Resize the filesystem
LOOP_DEVICE=$(losetup -j $IMAGE_NAME | awk -F: '{print $1}')
if [ -z "$LOOP_DEVICE" ]; then
    echo "Failed to find loop device for the image."
    exit 1
fi

echo "Resizing filesystem on $LOOP_DEVICE..."
sudo resize2fs $LOOP_DEVICE

# Unmount the image
echo "Unmounting the image..."
sudo umount $MOUNT_DIR

# Check the filesystem size
echo "Checking filesystem size..."
sudo e2fsck -f $IMAGE_NAME
sudo resize2fs -P $IMAGE_NAME

echo "Done!"