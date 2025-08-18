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
