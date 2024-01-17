#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
tool_dir = script_file_path.parent
bin_dir = tool_dir.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'

def remove_dirs(project, bug_version):
    project_name = project + '-' + bug_version
    project_dir = subjects_dir / project_name
    
    target_dirs = ['build', 'preprocessed']

    cmd = ['rm', '-rf']

    if project_dir.exists():
        for dir in target_dirs:
            d = project_dir / dir
            cmd.append(d)

            sp.call(cmd, cwd=main_dir)
            print(">> removed directory: {}".format(d))

            cmd.pop()
    else:
        print(">> jsoncpp project is not yet cloned")

def remove_gcda(project, bug_version):
    project_name = project + '-' + bug_version
    project_dir = subjects_dir / project_name

    cmd = [
        'find', './',
        '-type', 'f', '-name',
        '*.gcda', '-delete'
    ]

    sp.call(cmd, cwd=project_dir)

    print('>> deleted all gcda files')

def remove_gcno(project, bug_version):
    project_name = project + '-' + bug_version
    project_dir = subjects_dir / project_name

    cmd = [
        'find', './',
        '-type', 'f', '-name',
        '*.gcno', '-delete'
    ]

    sp.call(cmd, cwd=project_dir)

    print('>> deleted all gcno files')

def make_parser():
    parser = argparse.ArgumentParser(
        description='Remove built/generated files.'
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

if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    
    remove_dirs(args.project, args.bug_version)
    remove_gcno(args.project, args.bug_version)
    remove_gcno(args.project, args.bug_version)