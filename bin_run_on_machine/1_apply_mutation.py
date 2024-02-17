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
    template_name = sys.argv[7]
    template_dir = subjects_dir / template_name

    file_name = sys.argv[5] # json_reader.cpp or json_value.cpp
    file_path = sys.argv[6] # src/lib_json/json_reader.cpp or src/lib_json/json_value.cpp

    # APPLYING BUGFREE HERE
    bugfree_dir = main_dir / 'src/bug-versions-jsoncpp/bugFree'
    bugfree_json_reader = bugfree_dir / 'json_reader.cpp'
    bugfree_json_value = bugfree_dir / 'json_value.cpp'

    bug_json_reader = template_dir / 'src/lib_json/json_reader.cpp'
    bug_json_value = template_dir / 'src/lib_json/json_value.cpp'

    # replace bug files to bugfree files
    cmd = ['cp', bugfree_json_reader, bug_json_reader]
    sp.call(cmd, cwd=bin_dir)
    cmd = ['cp', bugfree_json_value, bug_json_value]
    sp.call(cmd, cwd=bin_dir)


    # APPLYING MUTATION HERE
    mutation_file = Path(sys.argv[1]) # file path to # json_value.MUT123.cpp
    
    mutation_name = sys.argv[2] # json_value.MUT123.cpp
    mutation_id = sys.argv[3]    # MUT123
    mutation_file_path = sys.argv[4] # src-lib_json-json_value.cpp-json_value.cpp


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
        
        # cmd = ['rm', target_file]
        # sp.call(cmd, cwd=bin_dir)

        # replace with mutation file
        cmd = ['cp', mutation_file, target_file]
        sp.call(cmd, cwd=bin_dir)
        print('replace with mutation file: {}'.format(mutation_name))
