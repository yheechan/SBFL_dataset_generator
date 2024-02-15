#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import json
import sys

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'

extractor_exe = main_dir / 'bin' / 'tools' / 'extractor'

def extract_line2function(project_path, cpp_files):
    # preprocessed_dir = project_path / 'preprocessed'
    preprocessed_dir = project_path

    cmd = [extractor_exe]

    cnt = 0

    perFile_data = {}
    for file in cpp_files:
        cmd.append(file)

        process = sp.Popen(
            cmd, stdout=sp.PIPE, stderr=sp.STDOUT,
            cwd=preprocessed_dir, encoding='utf-8'
        )

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() != None:
                break
            line = line.strip()
            if line == '':
                continue

            data = line.split("##")
            # print("class: \t{}".format(data[0]))
            class_name = data[0]
            # print("function: \t{}".format(data[1]))
            function_name = data[1]
            # print("start line: \t{}".format(data[2]))
            start_line = data[2]
            # print("end line: \t{}".format(data[3]))
            end_line = data[3]
            # print("origin file: \t{}".format(data[4]))
            originated_file = data[4]
            file_data = originated_file.split(':')[0]
            route_data = file_data.split('/')
            mark = 0
            for i in range(len(route_data)-1, -1, -1):
                if route_data[i] in ['src', 'build', 'include']:
                    mark = i
                    break
                if route_data[i] in ['a']:
                    mark = i
                    break
            marked_path = '/'.join(route_data[mark:])
            # print("marked file: {}".format(marked_path))
            # print("targeted file: \t{}".format(data[5]))
            # print("***************\n")

            if not marked_path in perFile_data.keys():
                perFile_data[marked_path] = []
            
            full_function = class_name+'::'+function_name if class_name != 'None' else function_name
            data = (full_function, int(start_line), int(end_line))
            if not data in perFile_data[marked_path]:
                perFile_data[marked_path].append(data)
        
        print('>> extracted line2function from {}'.format(file))
        cmd.pop()
    
    return perFile_data

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()

def write_line2function(project_path, data, bug_version):
    data_dir = project_path / 'data'
    line2function_dir = data_dir / 'line2function'
    check_dir(data_dir)
    check_dir(line2function_dir)

    file_name = bug_version+'.line2function.json'

    file = line2function_dir / file_name

    with open(file, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    target_dir = subjects_dir / 'mytest'
    target_code = target_dir / 'a' / 'b' / 'mytest.c'
    pp_code = target_dir / 'pp.c'

    # extract line2function
    perFile_data = extract_line2function(target_dir, [pp_code])

    # write_line2function
    write_line2function(target_dir, perFile_data, sys.argv[1])
