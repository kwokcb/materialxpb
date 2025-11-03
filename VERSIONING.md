# MaterialX Protobuf Versioning Guide

## Overview

The MaterialX protobuf schema includes built-in versioning support to handle schema evolution and provide upgrade paths between versions.

## Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes (breaking changes)
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

Current version: **1.0.0**

## Schema Structure

```protobuf
message Version {
  uint32 major = 1;
  uint32 minor = 2;
  uint32 patch = 3;
}

message MaterialXDocument {
  Version schema_version = 1;     // Schema version
  repeated Attribute attributes = 2;
  repeated MaterialXElement elements = 3;
}
```

## Version Compatibility Rules

### Reading Documents

1. **Same major version**: - Always compatible
   - Example: v1.2.0 can read v1.0.0 and v1.3.0

2. **Older major version**: - Compatible with upgrade
   - Example: Current v2.0.0 can upgrade v1.x.x documents
   - Upgrade performed automatically during deserialization

3. **Newer major version**: Not compatible
   - Example: v1.x cannot read v2.x
   - Error thrown with message to upgrade software

### Writing Documents

Always writes with the current schema version defined in the code:
```python
SCHEMA_VERSION_MAJOR = 1
SCHEMA_VERSION_MINOR = 0
SCHEMA_VERSION_PATCH = 0
```

## How to Make Schema Changes

### 1. Adding a New Optional Field (Minor Version Bump)

```protobuf
message MaterialXElement {
  string name = 1;
  string type = 2;
  repeated Attribute attributes = 3;
  repeated MaterialXElement children = 4;
  
  // New optional field
  string description = 5;  // v1.1.0
}
```

**Impact**: 
- Older readers ignore the new field
- Newer readers use it if present
- No upgrade code needed

**Update version to**: 1.1.0

### 2. Deprecating a Field (Minor Version Bump + Reserved)

```protobuf
message MaterialXElement {
  string name = 1;
  string type = 2;
  repeated Attribute attributes = 3;
  repeated MaterialXElement children = 4;
  
  // Field 5 was 'old_field', now reserved
  reserved 5;
  reserved "old_field";
  
  string new_field = 6;  // Replacement
}
```

**Upgrade code needed**:
```python
@staticmethod
def upgrade_v1_to_v2(pb_doc):
    """Upgrade from v1.x to v2.x - migrate old_field to new_field"""
    for element in pb_doc.elements:
        if element.HasField('old_field'):
            element.new_field = element.old_field
            element.ClearField('old_field')
```

**Update version to**: 2.0.0 (breaking change)

### 3. Changing Field Type (Major Version Bump)

This is a **breaking change**. Use a new field number:

```protobuf
message MaterialXElement {
  string name = 1;
  string type = 2;
  
  // Old: map<string, string> attributes = 3;
  reserved 3;  // Reserve old field
  
  repeated Attribute attributes = 4;  // New field number
}
```

**Update version to**: 2.0.0

## Implementing Upgrades

### 1. Update the Schema Version Constants

```python
# materialx_serializer.py
SCHEMA_VERSION_MAJOR = 2  # Updated from 1
SCHEMA_VERSION_MINOR = 0
SCHEMA_VERSION_PATCH = 0
```

### 2. Add Upgrade Logic

```python
def _check_version_and_upgrade(self, pb_doc, mx):
    doc = mx.createDocument()
    
    if pb_doc.HasField('schema_version'):
        major = pb_doc.schema_version.major
        
        # Upgrade v1 to v2
        if major == 1 and SCHEMA_VERSION_MAJOR >= 2:
            VersionUpgrader.upgrade_v1_to_v2(pb_doc)
        
        # Upgrade v2 to v3
        if major == 2 and SCHEMA_VERSION_MAJOR >= 3:
            VersionUpgrader.upgrade_v2_to_v3(pb_doc)
    
    return doc
```

### 3. Implement the Upgrader

```python
class VersionUpgrader:
    @staticmethod
    def upgrade_v1_to_v2(pb_doc):
        """Upgrade document from v1.x to v2.x"""
        print(f"Upgrading document from v1.x to v2.x...")
        
        # Example: Convert old attribute format to new format
        for element in pb_doc.elements:
            # Perform migration logic here
            pass
        
        # Update version
        pb_doc.schema_version.major = 2
        pb_doc.schema_version.minor = 0
        pb_doc.schema_version.patch = 0
```

## Best Practices

### 1. Always Use Reserved for Removed Fields
```protobuf
reserved 5, 6, 10 to 15;  // Reserve field numbers
reserved "old_name", "deprecated_field";  // Reserve names
```

### 2. Never Reuse Field Numbers
Once a field number is used, never reuse it - mark it as reserved instead.

### 3. Add Optional Fields for Extensions
New fields should be optional (the default in proto3) to maintain backwards compatibility.

### 4. Document Changes in Comments
```protobuf
message MaterialXElement {
  string name = 1;
  string type = 2;
  repeated Attribute attributes = 3;
  repeated MaterialXElement children = 4;
  
  // Added in v1.1.0: Optional description field
  string description = 5;
  
  // Added in v1.2.0: Metadata support
  repeated Attribute metadata = 6;
}
```

### 5. Test Backwards Compatibility
Always test that new code can read old protobuf files:

```python
# Test reading v1.0.0 document with v1.1.0 code
old_doc = load_v1_0_document()
converter = ProtobufToMaterialX()
mx_doc = converter.convert(old_doc, mx)
# Should work without errors
```

## Version History

### v1.0.0 (Current)
- Initial versioned schema
- Changed from `map<>` to `repeated Attribute` for order preservation
- Added `Version` message
- Added `schema_version` to MaterialXDocument

## Example Usage

### Writing with Version Info
```python
from materialx_serializer import MaterialXToProtobuf

converter = MaterialXToProtobuf()
pb_doc = converter.convert(mx_doc)

# Version is automatically set
print(f"Schema version: {pb_doc.schema_version.major}."
      f"{pb_doc.schema_version.minor}."
      f"{pb_doc.schema_version.patch}")
```

### Reading with Version Check
```python
from materialx_serializer import ProtobufToMaterialX

converter = ProtobufToMaterialX()
try:
    mx_doc = converter.convert(pb_doc, mx)
except ValueError as e:
    print(f"Version error: {e}")
    # Document is too new, upgrade software
```

### Checking Version Programmatically
```python
from materialx_serializer import VersionUpgrader

version_str = VersionUpgrader.get_version_string(pb_doc)
print(f"Document version: {version_str}")

# Compare versions
result = VersionUpgrader.compare_versions(
    1, 0, 0,  # v1.0.0
    1, 2, 3   # v1.2.3
)
# result = -1 (first version is older)
```

## Future Considerations

When planning schema changes, consider:

1. **Migration complexity**: How difficult is it to upgrade old documents?
2. **Data loss**: Will any information be lost in the upgrade?
3. **Performance**: Will upgrades impact loading time significantly?
4. **Testing**: Can you test the upgrade path thoroughly?
5. **Documentation**: Are changes clearly documented for users?

## Questions?

For questions about versioning strategy or implementing upgrades, please refer to the Protocol Buffers documentation on schema evolution:
https://protobuf.dev/programming-guides/proto3/#updating
