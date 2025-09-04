#!/bin/zsh
# Build script for SCons with Bear to generate compile_commands.json

# Run Bear with SCons to capture compilation database
bear -- scons build=debug

echo "Build complete. Compilation database is in compile_commands.json."
