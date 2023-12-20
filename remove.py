#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent

def remove_dirs():
    target_dirs = [
        'build-1',
        'coverage',
        'data'
    ]

    cmd = ['rm', '-rf']

    for dir in target_dirs:
        d = main_dir / dir
        cmd.append(d)

        sp.call(cmd, cwd=main_dir)

        cmd.pop()
    
    print('>> removed directories')

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



if __name__ == '__main__':
    remove_dirs()
    remove_gcno()
    remove_gcda()
