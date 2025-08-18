#!/bin/bash
# Uninstall all installed Python packages starting with 'qutil'

set -e
set -x

# List all installed packages starting with qutil, ignoring case
packages=$(pip list --format=freeze | grep -i '^qutil' | cut -d= -f1)

if [ -z "$packages" ]; then
  echo "No qutil packages found."
  exit 0
fi

echo "Uninstalling: $packages"
pip uninstall -y $packages --break-system-packages