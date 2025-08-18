#!/bin/bash

set -e
set -x

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build wheels for all qutil-* directories
for dir in ${SCRIPT_DIR}/../qutil-*/; do
    if [ -d "$dir" ]; then
        echo "Building wheel for $dir..."
        pip wheel "$dir" --wheel-dir "$SCRIPT_DIR" --no-deps
    fi
done

# Install all qutil-* packages by name using --find-links, to mimic PyPI behavior
for whl in "$SCRIPT_DIR"/qutil*.whl; do
    if [ -f "$whl" ]; then
        pkg_name=$(basename "$whl" | sed -E 's/-[0-9].*$//')
        echo "Installing $pkg_name from $SCRIPT_DIR..."
        pip install --user "$pkg_name" --break-system-packages --find-links "$SCRIPT_DIR"
    fi
done

echo "All qutil-* wheel files built and installed"

pip freeze | grep '^qutil'