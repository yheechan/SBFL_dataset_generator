#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
music_exe = bin_dir / 'MUSIC' / 'music'

main_dir = bin_dir.parent
mutations_output_dir = main_dir / 'mutations'

template_dir = main_dir / 'subjects' / 'template'
build_tool = bin_dir / 'build_tool.sh'

def build_template():
    build_dir = template_dir / 'build'
    if not build_dir.exists():
        cmd = ['bash', build_tool]
        sp.call(cmd, cwd=template_dir)
    else:
        print('Template already built')
    
    compile_cmd_json = build_dir / 'compile_commands.json'
    if not compile_cmd_json.exists():
        print('compile_commands.json not found')
        exit(1)
    else:
        print('compile_commands.json found')
    
    return build_dir, compile_cmd_json

if __name__ == "__main__":
    build_dir, compile_cmd_json = build_template()

    if not mutations_output_dir.exists():
        mutations_output_dir.mkdir()
    
    template_dir = main_dir / 'subjects' / 'template'
    mytest_dir = main_dir / 'subjects' / 'mytest'
    jsoncpp_src = template_dir / 'src'
    lib_json_dir = jsoncpp_src / 'lib_json'
    
    target_files = [
        mytest_dir / 'mytest.c',
        # lib_json_dir / 'json_value.cpp',
        # lib_json_dir / 'json_reader.cpp',
    ]
    file_types = ['cpp', 'c', 'h', 'inl']

    bash_file = open('4_make_mutations.sh', 'w')
    bash_file.write('date\n')

    cnt = 0
    for file in target_files:

        if not file.exists():
            print('File not found: {}'.format(file))
            exit(1)
        dir_path = file.parent
        dir_path_str = '/'.join(str(dir_path).split('/')[8:])+'/'
        
        file_name = file.name
        ftype = file_name.split('.')[-1]
        if ftype not in file_types:
            print('Not a valid file type: {}'.format(file))
            exit(1)
        
        if dir_path_str.split('/')[0] == '':
            dir_path_str = ''
        output_dir_name = (dir_path_str + file_name).replace('/', '-')
        
        # make output directory for this file
        output_dir = main_dir / 'mutations' / output_dir_name
        if not output_dir.exists():
            output_dir.mkdir()
        
        if file_name == 'mytest.c':
            cmd = '{} {} -o {} -- & \n'.format(
                music_exe, file, output_dir
            )
            bash_file.write(cmd)
            continue
        
        # make mutations for this file into the output directory
        cmd = '{} {} -o {} -l 1 -p {} & \n'.format(
            music_exe, file, output_dir,
            compile_cmd_json
        )
        bash_file.write(cmd)

        if cnt % 5 == 0:
            bash_file.write("sleep 1s\n")
        cnt += 1
    
    bash_file.write('echo ssh done, waiting...\n')
    bash_file.write('date\n')
    bash_file.write('wait\n')
    bash_file.write('date\n')
    
    cmd = ['chmod', '+x', '4_make_mutations.sh']
    res = sp.call(cmd, cwd=bin_dir)
