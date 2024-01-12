#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
jsoncpp_dir = main_dir / 'jsoncpp'

def remove_dirs(onlyProject=False, withPreprocesed=False):
    target_dirs = ['build']
    if not onlyProject:
        target_dirs.append('coverage')
        target_dirs.append('data')

    if withPreprocesed:
        target_dirs.append('preprocessed')

    cmd = ['rm', '-rf']

    if jsoncpp_dir.exists():
        for dir in target_dirs:
            d = jsoncpp_dir / dir
            cmd.append(d)

            sp.call(cmd, cwd=main_dir)
            print(">> removed directory: {}".format(d))

            cmd.pop()
    else:
        print(">> jsoncpp project is not yet cloned")

def remove_gcda():
    cmd = [
        'find', './',
        '-type', 'f', '-name',
        '*.gcda', '-delete'
    ]

    sp.call(cmd, cwd=main_dir)

    print('>> deleted all gcda files')

def remove_gcno():
    cmd = [
        'find', './',
        '-type', 'f', '-name',
        '*.gcno', '-delete'
    ]

    sp.call(cmd, cwd=main_dir)

    print('>> deleted all gcno files')

def make_parser():
    parser = argparse.ArgumentParser(
        description='Remove built/generated files.'
    )

    parser.add_argument(
        '--onlyProject',
        required=False,
        action='store_true',
        help='whether to delete coverage and data files'
    )

    parser.add_argument(
        '--withPreprocessed',
        required=False,
        action='store_true',
        help='whether to delete coverage and data files'
    )

    parser.add_argument(
        '--all',
        required=False,
        action='store_true',
        help='whether to delete coverage and data files'
    )

    return parser

if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()

    if args.all:
        args.onlyPreprocessed = True
    
    remove_dirs(onlyProject=args.onlyProject, withPreprocesed=args.withPreprocessed)
    remove_gcno()
    remove_gcda()
