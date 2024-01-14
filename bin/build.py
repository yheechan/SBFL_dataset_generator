#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

from utils import myExecutor as xx
from utils import myWriter as ww
from utils import myHelper as hh

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'

def build(project_dir, dir_name, preprocessed=False):
    build_dir = project_dir / dir_name

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

    if preprocessed:
        cmd[2] += ' --save-temps'

    sp.call(cmd, cwd=build_dir)

    print('>> built project')

    return build_dir

def make(project_dir, dir_name):
    build_dir = project_dir / dir_name
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

def compile_fuzzer(project_dir, dir_name):
    build_dir = project_dir / dir_name
    fuzzer = build_dir / 'jsoncpp_fuzzer'
    link_file = build_dir / 'src/lib_json/libjsoncpp.a'
    fuzz_dir = project_dir / 'src/test_lib_json'

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

def remove(project, bug_version, onlyProject=False, onlyPreprocesed=False):

    cmd = ['./remove.py', '--project', project, '--bug_version', bug_version]
    if onlyProject:
        cmd.append('--onlyProject')
    
    if onlyPreprocesed:
        cmd.append('--withPreprocessed')

    sp.call(cmd, cwd=bin_dir)
    print(">> removed currently build project")

def check_project_cloned(project, bug_version):
    project_name = project + '-' + bug_version
    project_path = subjects_dir / project_name
    if not project_path.exists():
        # clone project
        exe = './clone_'+project+'.py'
        cmd = [exe, '--project', project, '--bug_version', bug_version]
        res = sp.call(cmd, cwd=bin_dir)
        if res == 1:
            exit(1)
        print(">> completely cloned project: {}".format(project_name))
    return project_path

def check_extractor_built(name):
    extractor_bin = bin_dir / name
    if not extractor_bin.exists():
        # build extractor
        exe = 'build_'+name+'.sh'
        cmd = ['bash', exe]
        res = sp.call(cmd, cwd=bin_dir)
        if res == 1:    
            exit(1)
        print(">> built extractor")

def make_parser():
    parser = argparse.ArgumentParser(
        description='Build and Compile targets.'
    )

    parser.add_argument(
        '--project',
        type=str,
        required=True,
        help='project name'
    )

    parser.add_argument(
        '--bug_version',
        type=str,
        required=True,
        help='bug version'
    )

    parser.add_argument(
        '--preprocessed',
        required=False,
        action='store_true',
        help='for building with preprocessed files'
    )

    parser.add_argument(
        '--onlyProject',
        required=False,
        action='store_true',
        help='for deleting only Project'
    )

    parser.add_argument(
        '--withPreprocessed',
        required=False,
        action='store_true',
        help='for deleting only preprocessed project'
    )

    return parser

if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()

    name = 'build'
    preprocessed = 'preprocessed'

    project_dir = check_project_cloned(args.project, args.bug_version)
    check_extractor_built('extractor')

    remove(
        args.project, args.bug_version,
        onlyProject=args.onlyProject, onlyPreprocesed=True
    )

    if args.withPreprocessed:
        # build preprocessed project
        build(project_dir, preprocessed, preprocessed=True)
        make(project_dir, preprocessed)

        ii_files = xx.get_ii_files(project_dir)
        cpp_files = xx.change_ii_to_cpp(project_dir, ii_files)

        perFile_data = xx.extract_line2method(project_dir, cpp_files)
        ww.write_line2method(project_dir, perFile_data, args.bug_version)
        remove(
            args.project, args.bug_version,
            onlyProject=args.onlyProject, onlyPreprocesed=True
        )

    # build coverage project
    build(project_dir, name)
    make(project_dir, name)
    # copy_files(name)
    compile_fuzzer(project_dir, name)
