import os
import sys
import pytest

# Add parent directory to sys.path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from source import materialx_serializer

try:
    import MaterialX as mx
    HAS_MATERIALX = True
except ImportError:
    HAS_MATERIALX = False

data_dir = os.path.join(os.path.dirname(__file__), '../source/data')

data_files = [
    'standard_surface_chess_set.json',
    'standard_surface_chess_set.mtlx',
    'standard_surface_chess_set.mxpb',
    'standard_surface_chess_set_converted.mtlx',
    'standard_surface_chess_set_from_pb.mtlx',
    'unlit_cross.json',
    'unlit_cross.mtlx',
    'unlit_cross.mxpb',
    'unlit_cross_converted.mtlx',
    'unlit_cross_from_pb.mtlx',
]

def get_file_path(filename):
    return os.path.join(data_dir, filename)


# Test that all files exist
@pytest.mark.parametrize('filename', data_files)
def test_file_exists(filename):
    assert os.path.exists(get_file_path(filename)), f"File {filename} does not exist."


# Test that JSON files are valid JSON
import json
@pytest.mark.parametrize('json_file', [f for f in data_files if f.endswith('.json')])
def test_json_valid(json_file):
    with open(get_file_path(json_file), 'r') as f:
        json_data = f.read()
    try:
        obj = json.loads(json_data)
    except Exception as e:
        pytest.fail(f"Invalid JSON in {json_file}: {e}")


# Test that .mxpb files can be parsed into protobuf objects
@pytest.mark.parametrize('mxpb_file', [f for f in data_files if f.endswith('.mxpb')])
def test_mxpb_to_protobuf(mxpb_file):
    with open(get_file_path(mxpb_file), 'rb') as f:
        pb_data = f.read()
    pb_doc = materialx_serializer.Util.from_string(pb_data)
    assert pb_doc is not None


# Test that .mtlx files can be parsed and converted to protobuf (requires MaterialX)
@pytest.mark.parametrize('mtlx_file', [f for f in data_files if f.endswith('.mtlx')])
def test_materialx_to_protobuf(mtlx_file):
    if not HAS_MATERIALX:
        pytest.skip("MaterialX Python API not installed")
    doc = mx.createDocument()
    mx.readFromXmlFile(doc, get_file_path(mtlx_file))
    pb_doc = materialx_serializer.MaterialXToProtobuf().convert(doc)
    assert pb_doc is not None

# Test mtlx -> protobuf -> mtlx equivalence
@pytest.mark.parametrize('mtlx_file', [f for f in data_files if f.endswith('.mtlx')])
def test_mtlx_protobuf_mtlx_equivalence(mtlx_file):
    if not HAS_MATERIALX:
        pytest.skip("MaterialX Python API not installed")
    # Read original mtlx
    doc1 = mx.createDocument()
    mx.readFromXmlFile(doc1, get_file_path(mtlx_file))
    # Convert to protobuf
    pb_doc = materialx_serializer.MaterialXToProtobuf().convert(doc1)
    # Convert back to MaterialX
    doc2 = materialx_serializer.ProtobufToMaterialX().convert(pb_doc, mx)
    # Check equivalence
    options = mx.ElementEquivalenceOptions()
    is_same, differences = doc1.isEquivalent(doc2, options)
    assert is_same, f"Documents are not equivalent for {mtlx_file}: {differences}"

# Test mxpb -> mtlx conversion
@pytest.mark.parametrize('mxpb_file', [f for f in data_files if f.endswith('.mxpb')])
def test_mxpb_to_mtlx(mxpb_file):
    if not HAS_MATERIALX:
        pytest.skip("MaterialX Python API not installed")
    with open(get_file_path(mxpb_file), 'rb') as f:
        pb_data = f.read()
    pb_doc = materialx_serializer.Util.from_string(pb_data)
    doc = materialx_serializer.ProtobufToMaterialX().convert(pb_doc, mx)
    # Check that doc is a MaterialX document
    assert hasattr(doc, 'getVersionString'), f"Conversion failed for {mxpb_file}"
