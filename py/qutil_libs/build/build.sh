#!/bin/bash 
set -e
set -x

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build wheels for all qutil-* directories

# Ignore qutil-xxx template directory
for dir in ${SCRIPT_DIR}/../qutil-*/; do
    if [ -d "$dir" ]; then
        case "$dir" in
            *qutil-xxx*/)
                echo "Skipping template $dir"
                continue
                ;;
        esac
        echo "Building wheel for $dir..."
        pip3 wheel "$dir" --wheel-dir "$SCRIPT_DIR" --no-deps
    fi
done
