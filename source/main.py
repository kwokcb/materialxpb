# main.py
from materialx_serializer import MaterialXToProtobuf, ProtobufToMaterialX, Util
import MaterialX as mx
import argparse, os, sys

def write_file(input_path, output_folder, suffix, content, debug_print, mode='w'):
    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)
    output_file = f"{name}{suffix}"
    if output_folder:
        output_file = os.path.join(output_folder, output_file)
    else:
        output_file = os.path.join(os.path.dirname(input_path), output_file)
    if debug_print:
        print(f'Writing file: {output_file}')
    with open(output_file, mode) as f:
        f.write(content)
    return output_file

def compare_mtlx_documents(doc1, doc2):
    options = mx.ElementEquivalenceOptions()
    is_same, differences = doc1.isEquivalent(doc2, options)
    if not is_same:
        print("Differences found between MaterialX documents:")
        for diff in differences:
            print(diff)
    print("Documents are equivalent:", is_same)
    return is_same, differences

def main():
    parser = argparse.ArgumentParser(description='Convert MaterialX documents to and from Protobuf format.')
    parser.add_argument(dest="inputFile", help="Path of the input MaterialX document or folder.")
    parser.add_argument("-j", "--json", action="store_true", help="Output JSON representation of the Protobuf document.")
    parser.add_argument("-cb", "--convert_back", action="store_true", help="Convert back to MaterialX after Protobuf conversion.")
    parser.add_argument("-wm", "--write_mermaid", action="store_true", help="Output Mermaid diagram of the Protobuf document.")
    parser.add_argument('-of', '--output_folder', type=str, help='Output folder for converted files.')

    args = parser.parse_args()
    input_file = args.inputFile

    convert_from_mtlx = input_file.lower().endswith('.mtlx')
    convert_from_protobuf = input_file.lower().endswith('.mxpb')
    write_mermaid = args.write_mermaid if args.write_mermaid else False

    pb_doc = None
    write_json = args.json if args.json else False
    output_folder = args.output_folder if args.output_folder else None

    # Protobuf to MaterialX conversion
    if convert_from_protobuf:
        print('Reading Protobuf file:', input_file)
        data = None
        with open(input_file, 'rb') as f:
            data = f.read()
        pb_doc = Util.from_string(data)
        if not pb_doc:
            print('Error: Failed to parse Protobuf document.')
            sys.exit(1)

        # Convert to MaterialX
        converter = ProtobufToMaterialX()
        pb_version = pb_doc.schema_version
        mtlx_version = mx.getVersionString()
        print(f'Converting Protobuf document using schema version {pb_version.major}.{pb_version.minor}.{pb_version.patch} and MaterialX {mtlx_version}...')
        doc = converter.convert(pb_doc, mx)

        # Write out MaterialX file
        new_doc_string = mx.writeToXmlString(doc)
        write_file(input_file, output_folder, '_from_pb.mtlx', new_doc_string, True)

    # MaterialX to Protobuf conversion
    if convert_from_mtlx:
        convert_back = args.convert_back if args.convert_back else False

        print('Reading MaterialX file:', input_file)
        doc = mx.createDocument()
        mx.readFromXmlFile(doc, input_file)

        # Convert and save
        converter = MaterialXToProtobuf()
        print('Converting MaterialX document to Protobuf format...')
        pb_doc = converter.convert(doc)
        content = Util.to_string(pb_doc)
        write_file(input_file, output_folder, '.mxpb', content, True, mode='wb')

        # Convert back to MaterialX
        if convert_back:
            converter2 = ProtobufToMaterialX()
            new_doc = converter2.convert(pb_doc, mx)            
            is_same, messages = compare_mtlx_documents(doc, new_doc)
            new_doc_string = mx.writeToXmlString(new_doc)            
            write_file(input_file, output_folder, '_converted.mtlx', new_doc_string, True)

    if pb_doc: 
        if write_mermaid:
            mermaid_code = Util.generate_mermaid_diagram(pb_doc)    
            #markdown = '\n```mermaid\n' + mermaid_code + '\n```\n'
            markdown = mermaid_code
            write_file(input_file, output_folder, '_diagram.mmd', markdown, True)

        if write_json:
            json_str = Util.to_json(pb_doc, indent=2)
            write_file(input_file, output_folder, '.json', json_str, True)

        debug_pb_doc = False
        if debug_pb_doc:
            Util.debug_inspect_simple(pb_doc)    


if __name__ == "__main__":
    main()