#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent

def build(dir_name):
    build_dir = main_dir / dir_name

    if not build_dir.exists():
        build_dir.mkdir()
    
    cmd = [
        'cmake',
        '-DCMAKE_CXX_COMPILER=clang++',
        '-DCMAKE_CXX_FLAGS=-O0 -fprofile-arcs -ftest-coverage -g -fno-omit-frame-pointer -gline-tables-only -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION -fsanitize=address,undefined -fsanitize-address-use-after-scope -fsanitize=fuzzer-no-link',
        '-DBUILD_SHARED_LIBS=OFF', '-G',
        'Unix Makefiles',
        '../'
    ]
    sp.call(cmd, cwd=build_dir)

    print('>> built project')

    return build_dir

def make(dir_name):
    build_dir = main_dir / dir_name

    cmd = ['make']
    sp.call(cmd, cwd=build_dir)
    
    print('>> compiled project')

def copy_files(dir_name):
    build_dir = main_dir / dir_name

    cmd = ['cp']
    files = [
        '../src/test_lib_json/fuzz.dict',
        '../test-cases/tc-integeroverflow',
        '../test-cases/tc-heapoverflow',
        '../bin/run_fuzzer-1.sh'
    ]

    for file in files:
        cmd.append(file)
        cmd.append('./')

        sp.call(cmd, cwd=build_dir)

        cmd.pop()
        cmd.pop()
    
    print('>> copied needed files to build directory')

def compile_fuzzer(dir_name):
    build_dir = main_dir / dir_name
    fuzzer = build_dir / 'jsoncpp_fuzzer'
    link_file = build_dir / 'src/lib_json/libjsoncpp.a'
    fuzz_dir = main_dir / 'src/test_lib_json'

    cmd = [
        'clang++', '-O0',
        '-fprofile-arcs', '-ftest-coverage', '-g',
        '-fno-omit-frame-pointer', '-gline-tables-only',
        '-DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION',
        '-fsanitize=address,undefined',
        '-fsanitize-address-use-after-scope',
        '-fsanitize=fuzzer-no-link',
        '-I../../include', '-fsanitize=fuzzer',
        './fuzz.cpp', '-o', fuzzer, link_file
    ]

    sp.call(cmd, cwd=fuzz_dir)

    print('>> compiled fuzzer')

def only_make_tester(dir_name):
    build_dir = main_dir / dir_name
    test_dir = build_dir / 'src/test_lib_json'

    cmd = ['make']
    sp.call(cmd, cwd=test_dir)
    print('>> re-compiled jsoncpp_test')

    pass

def remove(onlyProject):
    cmd = ['./remove.py']
    if onlyProject:
        cmd.append('--onlyProject')
    sp.call(cmd, cwd=bin_dir)
    print(">> removed currently build project")

def chVersion(v):
    cmd = ['./chVersion.py', '--version', str(v)]
    res = sp.call(cmd, cwd=bin_dir)
    if res == 1:
        exit(1)

def make_parser():
    parser = argparse.ArgumentParser(
        description='Build and Compile targets.'
    )

    parser.add_argument(
        '--onlyTester',
        required=False,
        action='store_true',
        help='for re-compiling tester'
    )

    parser.add_argument(
        '--version',
        type=int,
        default=0,
        help='Converts JsonCPP project to User Selected Version. (Default: 0 which is bugFree version.)'
    )

    parser.add_argument(
        '--onlyProject',
        required=False,
        action='store_true',
        help='for deleting only Project'
    )

    return parser

if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()

    name = 'build'
    if args.onlyTester:
        only_make_tester(name)
    else:
        remove(args.onlyProject)
        chVersion(args.version)
        build(name)
        make(name)
        copy_files(name)
        compile_fuzzer(name)
