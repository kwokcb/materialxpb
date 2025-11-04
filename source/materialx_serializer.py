"""
@file materialx_serializer.py
@brief MaterialX Protobuf serialization and deserialization utilities.
@details
- Defines classes to convert MaterialX documents to and from Protobuf format.
- Provides utility functions for inspecting and debugging Protobuf documents.
- Requires the MaterialX Python API and the generated Protobuf Python module.
"""
import materialx_pb2 as pb
from google.protobuf.json_format import MessageToJson, MessageToDict

# Current schema version
SCHEMA_VERSION_MAJOR = 1
SCHEMA_VERSION_MINOR = 39
SCHEMA_VERSION_PATCH = 4

class MaterialXToProtobuf:
    """
    @brief Converter class to transform MaterialX document objects into Protobuf MaterialXDocument messages.
    @details
    - Traverses the MaterialX document structure and constructs the corresponding Protobuf message hierarchy.
    - Handles attributes and child elements recursively.
    - Usage:
        converter = MaterialXToProtobuf()
        pb_doc = converter.convert(mx_doc)
    - Where `mx_doc` is a MaterialX document object.
    """
    
    def convert(self, doc):
        """
        @brief Convert a MaterialX document object to a Protobuf MaterialXDocument message.
        @param doc The MaterialX document object to convert.
        @return The resulting Protobuf MaterialXDocument message.
        """
        pb_doc = pb.MaterialXDocument()
        
        # Set schema version
        pb_doc.schema_version.major = SCHEMA_VERSION_MAJOR
        pb_doc.schema_version.minor = SCHEMA_VERSION_MINOR
        pb_doc.schema_version.patch = SCHEMA_VERSION_PATCH
        
        # Store MaterialX version if available
        try:
            import MaterialX as mx
        except:
            pass
        
        for name in doc.getAttributeNames():
            attr = pb_doc.attributes.add()
            attr.key = name
            attr.value = doc.getAttribute(name)
        
        # Convert all root-level elements
        for child in doc.getChildren():
            pb_element = self._convert_element(child)
            pb_doc.elements.append(pb_element)
            
        return pb_doc
    
    def _convert_element(self, mx_elem):
        """
        @brief Recursively convert a MaterialX element to a Protobuf MaterialXElement.
        @param mx_elem The MaterialX element to convert.
        @return The resulting Protobuf MaterialXElement message.
        """
        pb_elem = pb.MaterialXElement()
        pb_elem.name = mx_elem.getName()
        pb_elem.type = mx_elem.getCategory()
        
        # Copy all attributes preserving order
        for name in mx_elem.getAttributeNames():
            attr = pb_elem.attributes.add()
            attr.key = name
            attr.value = mx_elem.getAttribute(name)
        
        # Recursively convert children
        for child in mx_elem.getChildren():
            pb_child = self._convert_element(child)
            pb_elem.children.append(pb_child)
            
        return pb_elem

class ProtobufToMaterialX:
    """
    @brief Converter class to transform Protobuf MaterialXDocument messages back into MaterialX document objects.
    @details
    - Traverses the Protobuf message structure and reconstructs the corresponding MaterialX document hierarchy.
    - Handles attributes and child elements recursively.
    - Requires the MaterialX Python API to create and manipulate document elements.
    - Usage:
        converter = ProtobufToMaterialX()
        mx_doc = converter.convert(pb_doc, mx)
    - Where `pb_doc` is a MaterialXDocument Protobuf message and `mx`
        is the MaterialX Python module.        
    """

    def convert(self, pb_doc, mx):
        """
        Convert a Protobuf MaterialXDocument message to a MaterialX document object.
        @param pb_doc The Protobuf MaterialXDocument message to convert.
        @param mx The MaterialX Python module for document creation.
        @return The reconstructed MaterialX document object.
        """
        # Check version compatibility and upgrade if needed
        doc = self._check_version_and_upgrade(pb_doc, mx)
        
        for pb_attribute in pb_doc.attributes:
            doc.setAttribute(pb_attribute.key, pb_attribute.value)

        for pb_element in pb_doc.elements:
            mx_element = self._convert_element(pb_element, doc, mx)
            
        return doc
    
    def _check_version_and_upgrade(self, pb_doc, mx):
        """
        @brief Check schema version and perform upgrades if necessary.
        @param pb_doc The Protobuf MaterialXDocument message.
        @param mx The MaterialX Python module.
        @return A new MaterialX document object.
        """
        doc = mx.createDocument()
        
        # Check if version is set
        if pb_doc.HasField('schema_version'):
            major = pb_doc.schema_version.major
            minor = pb_doc.schema_version.minor
            patch = pb_doc.schema_version.patch
            
            # Version compatibility check
            if major > SCHEMA_VERSION_MAJOR:
                raise ValueError(
                    f"Document schema version {major}.{minor}.{patch} is newer than "
                    f"supported version {SCHEMA_VERSION_MAJOR}.{SCHEMA_VERSION_MINOR}.{SCHEMA_VERSION_PATCH}. "
                    f"Please upgrade your software."
                )
            
            # Perform upgrades for older versions
            if major < SCHEMA_VERSION_MAJOR:
                print(f"Warning: Upgrading document from version {major}.{minor}.{patch} "
                      f"to {SCHEMA_VERSION_MAJOR}.{SCHEMA_VERSION_MINOR}.{SCHEMA_VERSION_PATCH}")
                # Add upgrade logic here when needed
                # self._upgrade_v0_to_v1(pb_doc)            
        else:
            # No version info - assume oldest supported version
            print("Warning: Document has no schema version information. Assuming legacy format.")
        
        return doc
    
    def _convert_element(self, pb_elem, parent, mx):
        """
        @brief Recursively convert a Protobuf MaterialXElement to a MaterialX element.
        @param pb_elem The Protobuf MaterialXElement message to convert.
        @param parent The parent MaterialX element to which the new element will be added.
        @param mx The MaterialX Python module for element creation.
        @return The newly created MaterialX element.
        """
        # Create element
        #print('Creating element:', pb_elem.type, pb_elem.name)
        mx_elem = parent.addChildOfCategory(pb_elem.type, pb_elem.name)
        
        # Set all attributes preserving order
        for attr in pb_elem.attributes:
            #print(' Setting attribute:', attr.key, '=', attr.value)
            mx_elem.setAttribute(attr.key, attr.value)
        
        # Recursively convert children
        for pb_child in pb_elem.children:
            child_elem = self._convert_element(pb_child, mx_elem, mx)
            #print(' Adding child element:', child_elem.getCategory(), child_elem.getName())
            
        return mx_elem
    
class Util:
    def from_string(data):
        """Convert string data to Protobuf document."""              
        pb_doc = pb.MaterialXDocument()
        pb_doc.ParseFromString(data)
        return pb_doc

    def to_string(pb_doc):
        """Convert Protobuf document to string."""              
        return (pb_doc.SerializeToString())

    def to_json(pb_doc, indent=2):
        """Convert Protobuf document to JSON string."""
        return MessageToJson(pb_doc, indent)

    """
    @class Util
    @brief Utility class for inspecting and debugging Protobuf MaterialXDocument messages.
    @details
    - Print the protobuf document structure in various formats.
    - Generate Mermaid diagrams for visualization of the document hierarchy.
    """
    @staticmethod
    def debug_inspect(pb_doc, max_depth=10, _current_depth=0):
        
        data = MessageToDict(pb_doc)
        
        def print_element(element, depth):
            indent = "  " * depth
            name = element.get('name', 'unnamed')
            elem_type = element.get('type', 'no-type')
            print(f"{indent}{name} ({elem_type})")
            # Print attributes (now a list of dicts)
            attrs = element.get('attributes', [])
            for attr in attrs:
                key = attr.get('key', '')
                value = attr.get('value', '')
                print(f"{indent}  │ {key}: {value}")
            # Print children recursively
            children = element.get('children', [])
            if children:
                print(f"{indent}  └─ Children ({len(children)}):")
                for child in children:
                    print_element(child, depth + 2)
        
        pb_version = pb_doc.schema_version
        print("Schema Version:", f"{pb_version.major}.{pb_version.minor}.{pb_version.patch}")

        attribs = ", ".join([f"{attr.get('key', '')}={attr.get('value', '')}" for attr in data.get('attributes', [])])
        print("Document:" + (f" [{attribs}]" if attribs else ""))

        for element in data.get('elements', []):
            print_element(element, 0)
        
        return data

    @staticmethod
    def debug_inspect_compact(pb_doc, max_depth=10, _current_depth=0):
        
        data = MessageToDict(pb_doc)

        def print_attributes(element, depth):
            indent = "  " * depth
            name = element.get('name', '')
            elem_type = element.get('type', '')
            if elem_type: 
                elem_type = f'({elem_type})'
            attrs = element.get('attributes', [])
            attrs_preview = ", ".join([f"{attr.get('key', '')}={attr.get('value', '')}" for attr in attrs[:2]])
            if attrs_preview:
                attrs_preview = f" [{attrs_preview}]"
            print(f"{indent}{name} {elem_type}{attrs_preview}")

        def print_element(element, depth):
            if depth > max_depth:
                return
            # Compact line showing key info
            print_attributes(element, depth)
            children_count = len(element.get('children', []))

            # Recursively print children
            for child in element.get('children', []):
                print_element(child, depth + 1)
        
        pb_version = pb_doc.schema_version
        print("Schema Version:", f"{pb_version.major}.{pb_version.minor}.{pb_version.patch}")

        attribs = ", ".join([f"{attr.get('key', '')}={attr.get('value', '')}" for attr in data.get('attributes', [])])
        print("Document:" + (f" [{attribs}]" if attribs else ""))

        for element in data.get('elements', []):
            print_element(element, 0)
        
        return data

    @staticmethod
    def debug_inspect_simple(pb_doc):
        
        def print_tree(element, prefix="", is_last=True):
            """Print tree structure with branches"""
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}{element.get('name', 'unnamed')} ({element.get('type', 'no-type')})")
            
            # Update prefix for children
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            # Print children
            children = element.get('children', [])
            for i, child in enumerate(children):
                print_tree(child, new_prefix, i == len(children) - 1)
        
        data = MessageToDict(pb_doc)
        
        pb_version = pb_doc.schema_version
        print("Schema Version:", f"{pb_version.major}.{pb_version.minor}.{pb_version.patch}")

        attribs = ", ".join([f"{attr.get('key', '')}={attr.get('value', '')}" for attr in data.get('attributes', [])])
        print("Document:" + (f" [{attribs}]" if attribs else ""))
        for i, element in enumerate(data.get('elements', [])):
            print_tree(element, "", i == len(data.get('elements', [])) - 1)
        
        return data    
    
    @staticmethod
    def generate_mermaid_diagram(pb_doc):
        """
        @brief Generate a Mermaid diagram (graph LR) from a protobuf document hierarchy.
        @details
        - Converts the protobuf message to a dict via google.protobuf.json_format.MessageToDict.
        - Creates one node per element labeled "name : type" (node IDs use the element name with spaces replaced by underscores).
        - Connects each element to its children with directed edges.
        @note This representation can be less readable when elements have many input/output children, as they are rendered as regular child nodes.
        @param pb_doc Protobuf message describing the document; expected schema:
            - elements: list of elements, each with:
                - name: str
                - type: str
                - children: list of elements (same structure)
        @return str Mermaid diagram source code.
        """
        data = MessageToDict(pb_doc)
        mermaid_lines = ["graph LR"]
        
        def add_mermaid_elements(element):
            node_id = element.get('name').replace(' ', '_')
            label = f"{element.get('name')} : {element.get('type')}"
            mermaid_lines.append(f"    {node_id}[{label}]")
            
            for child in element.get('children', []):
                child_id = child.get('name').replace(' ', '_')
                add_mermaid_elements(child)
                mermaid_lines.append(f"    {node_id} --> {child_id}")
        
        for element in data.get('elements', []):
            add_mermaid_elements(element)
        
        mermaid_code = "\n".join(mermaid_lines)
        
        return mermaid_code

class VersionUpgrader:
    """
    @class VersionUpgrader
    @brief Handles schema version upgrades for MaterialX protobuf documents.
    @details
    - Add upgrade methods for each major version transition.
    - Upgrade methods should modify the protobuf message in-place or return a new one.
    """
    
    @staticmethod
    def upgrade_v0_to_v1(pb_doc):
        """
        Example upgrade from version 0.x to 1.x
        @param pb_doc The protobuf document to upgrade (modified in-place).
        """
        # Example: If v1 added a new required field, set defaults here
        # if not pb_doc.HasField('new_field'):
        #     pb_doc.new_field = "default_value"
        pass
    
    @staticmethod
    def upgrade_v1_to_v2(pb_doc):
        """
        Example upgrade from version 1.x to 2.x
        @param pb_doc The protobuf document to upgrade (modified in-place).
        """
        # Example: If v2 renamed a field, copy old to new
        # for element in pb_doc.elements:
        #     if element.HasField('old_field_name'):
        #         element.new_field_name = element.old_field_name
        #         element.ClearField('old_field_name')
        pass
    
    @staticmethod
    def get_version_string(pb_doc):
        """Get version as a string (e.g., "1.0.0")"""
        if pb_doc.HasField('schema_version'):
            v = pb_doc.schema_version
            return f"{v.major}.{v.minor}.{v.patch}"
        return "unknown"
    
    @staticmethod
    def compare_versions(v1_major, v1_minor, v1_patch, v2_major, v2_minor, v2_patch):
        """
        Compare two versions.
        @return -1 if v1 < v2, 0 if equal, 1 if v1 > v2
        """
        if v1_major != v2_major:
            return -1 if v1_major < v2_major else 1
        if v1_minor != v2_minor:
            return -1 if v1_minor < v2_minor else 1
        if v1_patch != v2_patch:
            return -1 if v1_patch < v2_patch else 1
        return 0
