#!/bin/bash

set -e
set -x

./build.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Install all qutil-* packages by name using --find-links, to mimic PyPI behavior
for whl in "$SCRIPT_DIR"/qutil*.whl; do
    if [ -f "$whl" ]; then
        pkg_name=$(basename "$whl" | sed -E 's/-[0-9].*$//')
        echo "Installing $pkg_name from $SCRIPT_DIR..."
        pip3 install --user "$pkg_name" --break-system-packages --find-links "$SCRIPT_DIR"
    fi
done

echo "All qutil-* wheel files built and installed"

pip freeze | grep '^qutil'