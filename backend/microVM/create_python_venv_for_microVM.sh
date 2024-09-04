#!/bin/bash

# Settings
PYTHON_VERSION="3.10.12"
VENV_DIR="microVM_venv"

# 1. Add deadsnakes PPA and install Python
echo "Adding deadsnakes PPA and installing Python $PYTHON_VERSION..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev

# 2. Create a Python virtual environment with the newly installed Python
echo "Creating Python virtual environment $PYTHON_VERSION..."
/usr/bin/python3.10 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# 3. Install packages in the virtual environment
echo "Installing packages in the virtual environment..."
pip install --upgrade pip
pip install numpy

# 4. Modify shebang in the venv scripts
echo "Modifying shebang in venv scripts..."
NEW_SHEBANG="#!/root/microVM_venv/bin/python3"
FILES_TO_UPDATE=("$VENV_DIR/bin/pip" "$VENV_DIR/bin/pip3" "$VENV_DIR/bin/pip3.10")

for FILE in "${FILES_TO_UPDATE[@]}"; do
    if [ -f "$FILE" ]; then
        echo "Updating shebang in $FILE"
        sed -i "1s|.*|$NEW_SHEBANG|" "$FILE"
    else
        echo "$FILE not found, skipping..."
    fi
done

# 5. Deactivate the virtual environment
deactivate

# 6. Remove Python
echo "Removing Python $PYTHON_VERSION..."
sudo apt remove --purge -y python3.10 python3.10-venv python3.10-dev
sudo apt autoremove -y

echo "Process complete. Virtual environment is ready, and Python $PYTHON_VERSION has been removed."
