#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
versions_dir = bin_dir / 'versions'

lib_dir = main_dir / 'src/lib_json'

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
