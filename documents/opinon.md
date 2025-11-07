## Side-Bar: Musings

Protobuf offers some interesting features as a serialization format.

- **Structured data schema:**  
  - Protobuf defines a **pure data schema** (`.proto`) that can be compiled into strongly typed classes in different languages for API consistency.
  - Languages supported include: C++, Python, JavaScript, with extensions for languages like: Rust, Go, etc. 

- **Forward and backward compatibility:**  
  - Schema fields have unique numeric IDs along with `optional`, `reserved`, and `oneof` usage rules -- allowing fields to be added or deprecated without breaking older versions. 
  - This ensures compatibility at the *data model, API, and ABI* levels across versions and to be able to evolve as needed.

- **Binary representation:**  
  - Protobuf encodes data compactly and deterministically
    - The footprint is smaller and faster than XML or JSON by avoiding parsing and hierarchy building. 
    - Deterministic output ensures identical binary results for identical shading graphs — ideal for caching and network distribution. 
    - As sequencing is preserved this allows for deterministic binary equality checks.

- **Automatic multi-language APIs:**  
  - The `.proto` file acts as the single source of truth for generating bindings, removing the need for manual interfaces (e.g., `pybind11`).  
  
- **Thread-safe, parallelizable I/O:**  
  - Protobuf messages are thread safe for concurrent reads and can be serialized or deserialized in parallel.
  
- **Caveats**
  - Unlike `USDShade` it does not provide any *scene composition or variant logic* as it is not a stage system.  
  - Unlike `glTF` it does not support binary packaging nor runtime constraints.
  - Naturally things like scene composition, runtime binding, pipeline and delivery layers need to be handled at a higher level.

### Example: Protobuf Versioning

<pre>
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
</pre>

| Feature  | Example  | Purpose |  
| :-: | :-: | :-: |
| `Version` |  `Version schema_version`|  Semantic versioning of message schema (major.minor.patch) |   
| `optional`|  `optional string name = 2;`  |    Field may be omitted, safe for forward/backward compatibility |  
| `repeated`|  `repeated string connections = 5;`   |   Supports multiple inputs or multi-connections   |    
| `oneof`   |  `oneof value { ... }`   |  Only one of these fields may be set at a time; new values can be added safely in later versions |
| `reserved`|  `reserved 9,10; reserved "deprecated_field_name";` | Prevents reuse of field numbers or names from older versions, preserving compatibility  | 
| `Any` |   `google.protobuf.Any metadata = 8;`  |   Embeds arbitrary messages; allows future extensions without changing the core schema |  
| Schema evolution | `ShaderInputV1 → ShaderInputV2`  |    Added `description` and `int_value` fields without breaking backward compatibility|  


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
