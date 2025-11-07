

# MaterialX Protobuf Converter
[![GitHub Repo](https://img.shields.io/badge/GitHub-kwokcb%2Fmaterialxpb-181717?logo=github)](https://github.com/kwokcb/materialxpb) [![Build Status](https://github.com/kwokcb/materialxpb/actions/workflows/main.yml/badge.svg)](https://github.com/kwokcb/materialxpb/actions/workflows/main.yml)

Python utilities for converting MaterialX documents to and from Protocol Buffer format.

![Interop diagram](https://raw.githubusercontent.com/kwokcb/materialxpb/main/documents/images/flow.svg)

## What is Protocol Buffers?

[Protocol Buffers (protobuf)](https://protobuf.dev/) is Google's mechanism for serializing structured data.

## Benefits of Protocol Buffer Format

Protobuf focuses on data integrity, version safety, and cross-language consistency. Key benefits include:

- **Compact**: Binary format is smaller than XML
- **Fast**: Efficient serialization and deserialization
- **Cross-platform**: Language-agnostic format works across different platforms and programming languages
- **Typed**: Strong typing for data integrity
- **Versioning**: Built-in support for schema versioning and backward compatibility

## Overview

This project provides tools to:

- Convert MaterialX XML documents to Protocol Buffer format
- Serialize MaterialX documents to binary `.mxpb` files
- Export MaterialX documents to JSON format
- Convert Protocol Buffer documents back to MaterialX XML
- Generate visual diagrams of MaterialX document structure

## Prerequisites

### macOS Setup

Install Protocol Buffers compiler:
   ```bash
   brew install protobuf
   ```

### Windows Setup

Install Protocol Buffers compiler:
   ```bash
   choco install protoc
   ```

### Linux Setup   
Install Protocol Buffers compiler:
   ```bash
   sudo apt-get install -y protobuf-compiler
   ```

### Python Setup

1. Install Python protobuf library:
   ```bash
   pip install --only-binary=all protobuf
   ```
2. Install MaterialX Python library:
   ```bash
   pip install MaterialX
   ```

## Protocol Buffer Schema

The schema defines two main message types:

- **Attribute**: String key value pair. This is added to allow usage of repeated attributes as opposed to usage of maps. Maps in ProtoBuf are ordered which
is undesirable for MaterialX where attribute order matters for types such as node inputs and outputs as these define the signature of the node.
- **MaterialXElement**: Represents a MaterialX element with name, type, attributes, and child elements.
- **MaterialXDocument**: Represents the root of the element hierarchy and contains top-level attributes.

This schema reflects the simplicity of the MaterialX representation.

A schema **Version** message is also provided for version management including allowing for an upgrade mechanism if ever required. 

The schema is defined in the `materialx.proto` file.

## Generating Python Code from Proto Schema

Using the `materialx.proto`, Python bindings can be generated with the following command:

```bash
protoc --python_out=. materialx.proto
```

This generates `materialx_pb2.py` which contains the Protocol Buffer message classes.
These classes are used in the conversion logic to serialize and deserialize MaterialX documents.

## File Structure

```
- materialx.proto             # Protocol Buffer schema definition
- materialx_pb2.py            # Generated Python protobuf bindings
- materialx_serializer.py     # Conversion logic between MaterialX and Protobuf
- main.py                     # Command-line utility for conversion
- *.mtlx                      # Sample MaterialX documents
```


## Usage

### MaterialX to Protobuf Conversion

Convert a MaterialX document to Protobuf format:

```bash
python main.py path/to/<document>.mtlx
```

This command can optionally generate four output files:

1. **`.json`** - JSON representation
2. **`.mxpb`** - Binary Protocol Buffer format (compact serialization)
3. **`.mmd`** - Mermaid diagram
4. **`_converted.mtlx`** - Round-trip conversion back to MaterialX XML (for validation)

#### Example

```bash
python main.py standard_surface_chess_set.mtlx
```

Outputs:
- `standard_surface_chess_set.json` - JSON format
- `standard_surface_chess_set.mxpb` - Binary protobuf
- `standard_surface_chess_set_converted.mtlx` - Converted back to MaterialX

### Protobuf to MaterialX Conversion

Convert a Protobuf binary file back to MaterialX XML:

```bash
python main.py path/to/<document>.mxpb
```

This will generate a MaterialX XML file named `<document>_from_pb.mtlx`.

This command can optionally generate two output files:

1. **`.json`** - JSON representation
2. **`.mmd`** - Mermaid diagram

## Core Components

### materialx_serializer.py

#### MaterialXToProtobuf
Converts MaterialX documents to Protocol Buffer format:
- Extracts document-level attributes
- Traverses the MaterialX document 
  - Extracts element names, types, and attributes
  - Recursively converts child elements

#### ProtobufToMaterialX
Converts Protocol Buffer format back to MaterialX:
- Creates MaterialX document
- Reconstructs MaterialX document attributes
- Restores element hierarchy and attributes

#### Util
Utility functions for debugging and visualization:
- `from_string()` - PB doc from string
- `to_string()` - PB doc to string
- `to_json()` - PB doc to json
- `generate_mermaid_diagram()` - Generate Mermaid diagrams for visualization

## Sample Files

The repository includes sample MaterialX documents:
- `standard_surface_chess_set.mtlx` - Chess set with standard surface shader
- `unlit_cross.mtlx` - Simple unlit cross shader

Each sample includes its converted outputs as appropriate (`.json`, `.mxpb`, `_converted.mtlx`, `from_pb.mtlx`).

## Visualization

Enable Mermaid diagram generation in `main.py` by setting `write_mermaid = True`. This generates a `.md` file with a Mermaid diagram showing the document structure.

