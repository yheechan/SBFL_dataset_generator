#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
versions_dir = main_dir / 'src/bug-versions-jsoncpp'

jsoncpp_dir = main_dir / 'jsoncpp'
lib_dir = jsoncpp_dir / 'src/lib_json'

def change_version(stand_dir_nm):
    stand_dir = versions_dir / stand_dir_nm
    
    # get new version
    files = []
    for file in os.listdir(stand_dir):
        assert file == 'json_value.cpp' or file == 'json_reader.cpp'
        files.append(stand_dir / file)
    
    # remove old version
    value_file = lib_dir / 'json_value.cpp'
    reader_file = lib_dir / 'json_reader.cpp'
    cmd = [
        'rm', value_file, reader_file
    ]
    sp.call(cmd, cwd=main_dir)
    print(">> Removed old version file for value and reader.")

    # copy new version
    cmd = [
        'cp'
    ]
    cmd += files
    cmd.append(lib_dir)
    sp.call(cmd, cwd=main_dir)
    print(">> Copied new version to lib directory")

    # change main.cpp in test_lib_json
    og_main_file = jsoncpp_dir / 'src/test_lib_json/main.cpp'
    cmd = ['rm', og_main_file]
    sp.call(cmd, cwd=main_dir)
    new_main_file = main_dir / 'src' / 'main.cpp'
    cmd = ['cp', new_main_file, og_main_file]
    sp.call(cmd, cwd=main_dir)

    # change makefile
    og_make_file = jsoncpp_dir / 'CMakeLists.txt'
    new_main_file = main_dir / 'src' / 'CMakeLists.txt'
    cmd = ['rm', og_make_file]
    sp.call(cmd, cwd=main_dir)
    cmd = ['cp', new_main_file, og_make_file]
    sp.call(cmd, cwd=main_dir)
    
def make_parser():
    parser = argparse.ArgumentParser(
        description='Convert current project version to User Selected Version, specifically to reproduce a bug from a test-case.'
    )

    parser.add_argument(
        '--version',
        type=int,
        default=0,
        help='Converts JsonCPP project to User Selected Version. (Default: 0 which is bugFree version.)'
    )

    return parser

if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    name = 'bug'
    if args.version == 0:
        name += 'Free'
    else:
        name += str(args.version)
    
    if args.version < 0 or args.version > 4:
        print('>> [ERROR] there is no available version for {}'.format(name))
        exit(1)
    else:
        change_version(name)
    
    print(">>> [COMPLETE] finished changing jsoncpp to new version: {}".format(name))
