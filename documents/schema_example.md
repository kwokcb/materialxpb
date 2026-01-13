### Versioned Protobuf Schema for Shader Inputs

```protobuf
syntax = "proto3";

package shading;

import "google/protobuf/any.proto";

// -------------------------------------------------
// Semantic versioning message
// -------------------------------------------------
message Version {
  uint32 major = 1;
  uint32 minor = 2;
  uint32 patch = 3;
}

// -------------------------------------------------
// Version 1 of ShaderInput
// -------------------------------------------------
message ShaderInputV1 {
  Version schema_version = 1; // semantic version of this message

  optional string name = 2;
  string type = 3;
  string default_value = 4;

  repeated string connections = 5;

  oneof value {
float float_value = 6;
repeated float color3_value = 7;
  }

  google.protobuf.Any metadata = 8;

  // Reserved fields from v1 (to prevent reuse)
  reserved 9, 10;
  reserved "deprecated_field_name";
}

// -------------------------------------------------
// Version 2 of ShaderInput (evolved)
// -------------------------------------------------
message ShaderInputV2 {
  Version schema_version = 1; // still semantic versioned (e.g., 2.0.0)

  optional string name = 2;
  string type = 3;
  string default_value = 4;

  repeated string connections = 5;

  // Oneof extended to include int value
  oneof value {
float float_value = 6;
repeated float color3_value = 7;
int32 int_value = 11; // new field
  }

  // Optional new description field
  optional string description = 12;

  google.protobuf.Any metadata = 8;

  // Reserved fields carry over
  reserved 9, 10;
  reserved "deprecated_field_name";
}

// -------------------------------------------------
// Container for multiple shader inputs (nodes)
// -------------------------------------------------
message ShaderNode {
  string name = 1;

  Version schema_version = 2; // version of the node definition

  repeated ShaderInputV2 inputs = 3;

  google.protobuf.Any extensions = 4;
}
```

| Feature  | Example  | Purpose |  
| :-: | :-: | :-: |
| `Version` |  `Version schema_version`|  Semantic versioning of message schema (major.minor.patch) |
| `optional`|  `optional string name = 2;`|Field may be omitted, safe for forward/backward compatibility |  
| `repeated`|  `repeated string connections = 5;`|Supports multiple inputs or multi-connections|
| `oneof`|  `oneof value { ... }`|  Only one of these fields may be set at a time; new values can be added safely in later versions |
| `reserved`|  `reserved 9,10; reserved "deprecated_field_name";` | Prevents reuse of field numbers or names from older versions, preserving compatibility  | 
| `Any` |`google.protobuf.Any metadata = 8;`  |Embeds arbitrary messages; allows future extensions without changing the core schema |  
| Schema evolution | `ShaderInputV1 → ShaderInputV2`  |Added `description` and `int_value` fields without breaking backward compatibility|  


<svg xmlns="http://www.w3.org/2000/svg" width="700" height="400" font-family="Arial, sans-serif">
  <!-- V1 box -->
  <rect x="20" y="20" width="300" height="220" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="8" ry="8"/>
  <text x="30" y="40" font-weight="bold" font-size="16">ShaderInputV1 (v1.0.0)</text>
  <text x="30" y="65">schema_version: 1.0.0</text>
  <text x="30" y="85">optional name</text>
  <text x="30" y="105">type</text>
  <text x="30" y="125">default_value</text>
  <text x="30" y="145">repeated connections</text>
  <text x="30" y="165">oneof value { float_value, color3_value }</text>
  <text x="30" y="185">metadata (Any)</text>
  <text x="30" y="205" fill="#b22222">reserved: 9,10,'deprecated_field_name'</text>

  <!-- V2 box -->
  <rect x="380" y="20" width="300" height="260" fill="#bad2f0ff" stroke="#6e6a6aff" stroke-width="2" rx="8" ry="8"/>
  <text x="390" y="40" font-weight="bold" font-size="16">ShaderInputV2 (v2.0.0)</text>
  <text x="390" y="65">schema_version: 2.0.0</text>
  <text x="390" y="85">optional name</text>
  <text x="390" y="105">type</text>
  <text x="390" y="125">default_value</text>
  <text x="390" y="145">repeated connections</text>
  <text x="390" y="165">oneof value { float_value, color3_value, int_value }</text>
  <text x="390" y="185">optional description</text>
  <text x="390" y="205">metadata (Any)</text>
  <text x="390" y="225" fill="#b22222">reserved: 9,10,'deprecated_field_name'</text>

  <!-- Arrow from V1 to V2 -->
  <line x1="320" y1="130" x2="380" y2="130" stroke="#61b3ffff" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Arrowhead definition -->
  <defs>
<marker id="arrowhead" markerWidth="10" markerHeight="7"
refX="0" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#61b3ffff"/>
</marker>
  </defs>
</svg>
