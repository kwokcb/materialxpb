/*
 @licstart  The following is the entire license notice for the JavaScript code in this file.

 The MIT License (MIT)

 Copyright (C) 1997-2020 by Dimitri van Heesch

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 and associated documentation files (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge, publish, distribute,
 sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 @licend  The above is the entire license notice for the JavaScript code in this file
*/
var NAVTREE =
[
  [ "Materialx Protobuf API", "index.html", [
    [ "MaterialX Protobuf Converter", "index.html", "index" ],
    [ "MaterialX Protobuf Converter - C++ Version", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html", [
      [ "Features", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md1", null ],
      [ "Prerequisites", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md2", [
        [ "Required Libraries", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md3", null ]
      ] ],
      [ "Building", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md4", [
        [ "Generate Protobuf C++ Code", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md5", null ],
        [ "Build the Executable", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md6", null ],
        [ "Manual CMake Build", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md7", null ],
        [ "Specifying Library Paths", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md8", null ]
      ] ],
      [ "Usage", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md9", [
        [ "Convert MaterialX to Protobuf", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md10", null ],
        [ "Convert Protobuf to MaterialX", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md11", null ],
        [ "Additional Options", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md12", null ]
      ] ],
      [ "Command-Line Options", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md13", null ],
      [ "File Structure", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md14", null ],
      [ "Code Organization", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md15", [
        [ "MaterialXToProtobuf Class", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md16", null ],
        [ "ProtobufToMaterialX Class", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md17", null ],
        [ "Util Class", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md18", null ],
        [ "VersionUpgrader Class", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md19", null ]
      ] ],
      [ "Performance Notes", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md20", null ],
      [ "Troubleshooting", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md21", [
        [ "CMake cannot find MaterialX", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md22", null ],
        [ "CMake cannot find Protobuf", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md23", null ],
        [ "Linking errors on Windows", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md24", null ],
        [ "Missing DLLs at runtime (Windows)", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md25", null ]
      ] ],
      [ "Development", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md26", null ],
      [ "See Also", "md__d_1_2_work_2materialx_2materialxpb_2cpp_2_r_e_a_d_m_e.html#autotoc_md27", null ]
    ] ],
    [ "Brief Blurb", "md_opinon.html", null ],
    [ "Versioned Protobuf Schema for Shader Inputs", "md_schema__example.html", null ],
    [ "Packages", "namespaces.html", [
      [ "Package List", "namespaces.html", "namespaces_dup" ],
      [ "Package Members", "namespacemembers.html", [
        [ "All", "namespacemembers.html", null ],
        [ "Functions", "namespacemembers_func.html", null ],
        [ "Variables", "namespacemembers_vars.html", null ]
      ] ]
    ] ],
    [ "Classes", "annotated.html", [
      [ "Class List", "annotated.html", "annotated_dup" ],
      [ "Class Index", "classes.html", null ],
      [ "Class Members", "functions.html", [
        [ "All", "functions.html", null ],
        [ "Functions", "functions_func.html", null ]
      ] ]
    ] ],
    [ "Files", "files.html", [
      [ "File List", "files.html", "files_dup" ],
      [ "File Members", "globals.html", [
        [ "All", "globals.html", null ],
        [ "Functions", "globals_func.html", null ],
        [ "Variables", "globals_vars.html", null ]
      ] ]
    ] ]
  ] ]
];

var NAVTREEINDEX =
[
"annotated.html"
];

var SYNCONMSG = 'click to disable panel synchronisation';
var SYNCOFFMSG = 'click to enable panel synchronisation';