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
        sed -i "1s|.*|$NEW_SHEBANG|" "$FILE"
    else
        echo "$FILE not found, skipping..."
    fi
done
