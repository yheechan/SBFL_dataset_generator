#!/usr/bin/python3

import subprocess as sp
from pathlib import Path
import os
import argparse
from utils import myHelper as hh

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
src_dir = main_dir / 'src'

subject_dir = main_dir / 'subjects'

bug_versions_dir = src_dir / 'bug-versions-jsoncpp'

def clone_projects(project, bug_version):
    hh.check_dir(subject_dir)

    dir_name = project + '-' + bug_version
    dir_path = subject_dir / dir_name

    clone_cmd = [
        'git', 'clone',
        'https://github.com/open-source-parsers/jsoncpp.git',
        dir_name
    ]

    reset_cmd = ['git', 'reset', '--hard', '83946a2']

    sp.call(clone_cmd, cwd=subject_dir)
    sp.call(reset_cmd, cwd=dir_path)

def change_files(project, bug_version):
    project_name = project + '-' + bug_version
    project_path = subject_dir / project_name

    selected_bug_dir = bug_versions_dir / bug_version

    value_file = [
        project_path / 'src/lib_json/json_value.cpp',
        selected_bug_dir / 'json_value.cpp'
    ]
    reader_file = [
        project_path / 'src/lib_json/json_reader.cpp',
        selected_bug_dir / 'json_reader.cpp'
    ]
    test_main_file = [
        project_path / 'src/test_lib_json/main.cpp',
        src_dir / 'main.cpp'
    ]
    cmakeFile = [
        project_path / 'CMakeLists.txt',
        src_dir / 'CMakeLists.txt'
    ]

    # remove old version
    cmd = ['rm', value_file[0], reader_file[0], test_main_file[0], cmakeFile[0]]
    sp.call(cmd, cwd=project_path)

    # copy new version
    cmd = ['cp', value_file[1], value_file[0]]
    sp.call(cmd, cwd=project_path)
    cmd = ['cp', reader_file[1], reader_file[0]]
    sp.call(cmd, cwd=project_path)
    cmd = ['cp', test_main_file[1], test_main_file[0]]
    sp.call(cmd, cwd=project_path)
    cmd = ['cp', cmakeFile[1], cmakeFile[0]]
    sp.call(cmd, cwd=project_path)

def make_parser():
    parser = argparse.ArgumentParser(
        description='Clone projects from github.com'
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

    return parser

if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    project = 'jsoncpp'
    bug_version = ['bug1', 'bug2', 'bug3', 'bug4']

    clone_projects(args.project, args.bug_version)
    change_files(args.project, args.bug_version)
