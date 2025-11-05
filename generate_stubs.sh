#!/bin/bash
# Generate Python stub files (.pyi) for the materialxpb package

echo "Generating stub files..."
cd source
stubgen --include-docstrings -v -o . materialx_serializer.py
echo "Stub generation complete!"
