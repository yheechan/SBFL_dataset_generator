#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'

src_dir = main_dir / 'src'
bug_versions_dir = src_dir / 'bug-versions-jsoncpp'

subject_dir = main_dir / 'subjects'


def clone_jsoncpp(name):
    template_dir = subjects_dir / name

    clone_cmd = [
        'git', 'clone', 'https://github.com/open-source-parsers/jsoncpp.git', name
    ]

    reset_cmd = ['git', 'reset', '--hard', '83946a2']

    sp.call(clone_cmd, cwd=subjects_dir)
    sp.call(reset_cmd, cwd=template_dir)

def change_files(project):
    project_name = 'bugFree'
    selected_bug_dir = bug_versions_dir / project_name
    
    project_path = subjects_dir / project


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
    res = sp.call(cmd, cwd=project_path)
    print('remove old version: ', res)

    # copy new version
    cmd = ['cp', value_file[1], value_file[0]]
    sp.call(cmd, cwd=project_path)
    print('copy 1: ', res)

    cmd = ['cp', reader_file[1], reader_file[0]]
    sp.call(cmd, cwd=project_path)
    print('copy 2: ', res)

    cmd = ['cp', test_main_file[1], test_main_file[0]]
    sp.call(cmd, cwd=project_path)
    print('copy 3: ', res)

    cmd = ['cp', cmakeFile[1], cmakeFile[0]]
    sp.call(cmd, cwd=project_path)
    print('copy 4: ', res)

def get_mytest(name):
    upper_dir = main_dir.parent
    target_dir = upper_dir / name
    clone_cmd = ['cp', '-r', target_dir, subjects_dir]
    sp.call(clone_cmd, cwd=subjects_dir)

if __name__ == "__main__":
    if not subjects_dir.exists():
        subjects_dir.mkdir()

    clone_jsoncpp('template')
    change_files('template')

    cores = 8
    for x in range(cores):
        template_name = 'core{}'.format(x)
        clone_jsoncpp(template_name)
        change_files(template_name)

    # get_mytest('mytest')
