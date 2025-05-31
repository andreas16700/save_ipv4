#!/bin/bash

# Determine the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment using an absolute path
source "$SCRIPT_DIR/venv/bin/activate"

# Run the Python script using an absolute path
python "$SCRIPT_DIR/src/main.py"