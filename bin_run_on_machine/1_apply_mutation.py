#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import sys

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'
mytest_dir = subjects_dir / 'mytest'

if __name__ == "__main__":
    mutation_file = Path(sys.argv[1])
    
    mutation_name = sys.argv[2]

    file_info = mutation_name.split('.')
    mutation_id = sys.argv[3]
    mutation_file_path = sys.argv[4]
    file_name = sys.argv[5]
    # get all element except last one from file_path.parent.name.split('-')
    # and join them with '-'
    file_path = sys.argv[6]
    
    template_name = sys.argv[7]
    template_dir = subjects_dir / sys.argv[7]

    # print('mutation file path: {}'.format(mutation_file))
    # print('mutation_id: {}'.format(mutation_id))
    # print('file_name: {}'.format(file_name))
    # print('file_path: {}\n'.format(file_path))

    if file_name == 'mytest.c':
        target_dir = mytest_dir
        # rm target file
        target_file = target_dir / file_path
        if not target_file.exists():
            print('File not found: {}'.format(target_file))
            exit(1)
        
        cmd = ['rm', target_file]
        sp.call(cmd, cwd=bin_dir)

        # replace with mutation file
        cmd = ['cp', mutation_file, target_file]
        sp.call(cmd, cwd=bin_dir)
        print('replace with mutation file: {}'.format(mutation_name))
    else:
        target_dir = template_dir

        # rm target file
        target_file = target_dir / file_path
        if not target_file.exists():
            print('File not found: {}'.format(target_file))
            exit(1)
        
        cmd = ['rm', target_file]
        sp.call(cmd, cwd=bin_dir)

        # replace with mutation file
        cmd = ['cp', mutation_file, target_file]
        sp.call(cmd, cwd=bin_dir)
        print('replace with mutation file: {}'.format(mutation_name))
