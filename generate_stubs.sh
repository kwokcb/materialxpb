#!/bin/bash
# Generate Python stub files (.pyi) for the materialxpb package
# and C++ protobuf code

echo "Generating Python stub files..."
cd source
stubgen --include-docstrings -v -o . materialx_serializer.py
echo "Python stub generation complete!"

echo "Generating C++ protobuf code..."
protoc --cpp_out=../cpp materialx.proto
echo "C++ protobuf generation complete!"
