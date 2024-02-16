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
clangPP = Path('/usr/bin/clang++-13')

def clean_json_build_dir(project_dir, only_pp=False):
    if only_pp:
        pp_dir = project_dir / 'preprocessed'
        if pp_dir.exists():
            cmd = ['rm', '-rf', pp_dir]
            sp.call(cmd, cwd=main_dir)
            print('>> removed directory: {}'.format(pp_dir))
        return
    else:
        pp_dir = project_dir / 'preprocessed'
        if pp_dir.exists():
            cmd = ['rm', '-rf', pp_dir]
            sp.call(cmd, cwd=main_dir)
            print('>> removed directory: {}'.format(pp_dir))
        
        build_dir = project_dir / 'build'
        if build_dir.exists():
            cmd = ['rm', '-rf', build_dir]
            sp.call(cmd, cwd=main_dir)
            print('>> removed directory: {}'.format(build_dir))

def clean_mytest():
    target_dir = subjects_dir / 'mytest'
    clean = 'clean.sh'
    cmd = ['bash', clean]
    res = sp.call(cmd, cwd=target_dir)
    if res != 0:
        print('clean failed: {}'.format(res))
        exit(1)

def build_jsoncpp(project_dir, dir_name, preprocessed=False):
    build_dir = project_dir / dir_name

    if not build_dir.exists():
        build_dir.mkdir()
    
    cmd = [
        'cmake',
        '-DCMAKE_CXX_COMPILER={}'.format(clangPP),
        '-DCMAKE_CXX_FLAGS=-O0 -fprofile-arcs -ftest-coverage -g -fno-omit-frame-pointer -gline-tables-only -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION -fsanitize=address,undefined -fsanitize-address-use-after-scope -fsanitize=fuzzer-no-link',
        '-DBUILD_SHARED_LIBS=OFF', '-G',
        'Unix Makefiles',
        '../'
    ]

    if preprocessed:
        cmd[2] += ' --save-temps'

    res = sp.call(cmd, cwd=build_dir)
    if res != 0:
        print('cmake failed: {}'.format(res))
        exit(1)

    print('>> built project')

    return build_dir

def make_jsoncpp(project_dir, dir_name):
    build_dir = project_dir / dir_name
    cmd = ['make', '-j20']
    res = sp.call(cmd, cwd=build_dir)
    if res != 0:
        print('make failed: {}'.format(res))
        exit(1)
    print('>> compiled project')

def build_mytest_pp():
    target_dir = subjects_dir / 'mytest'
    target_code = target_dir / 'a' / 'b' / 'mytest.c'

    cmd = ['clang', '-E', target_code, '-o', target_dir / 'pp.c']
    res = sp.call(cmd, cwd=bin_dir, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    if res != 0:
        print('preprocessing code failed: {}'.format(res))
        exit(1)

def get_ii_files(project_path):
    cmd = [
        'find', '.', '-type',
        'f', '-name', '*.ii'
    ]

    preprocessed_dir = project_path / 'preprocessed'

    process = sp.Popen(
        cmd, stdout=sp.PIPE, stderr=sp.STDOUT,
        cwd=preprocessed_dir, encoding='utf-8'
    )

    ii_files = []
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() != None:
            break
        line = line.strip()
        if line == '':
            continue
        ii_files.append(line)
    
    return ii_files

def change_ii_to_cpp(project_path, ii_files):
    preprocessed_dir = project_path / 'preprocessed'

    cmd = ['mv']

    cpp_files = []
    if len(ii_files) != 0:
        for file in ii_files:
            cmd.append(file)
            cpp_file_name = file[:-2]+'cpp'
            cmd.append(cpp_file_name)
            cpp_files.append(cpp_file_name)

            res = sp.call(cmd, cwd=preprocessed_dir)

            cmd.pop()
            cmd.pop()
    else:
        cmd = [
            'find', '.', '-type',
            'f', '-name', '*.cpp'
        ]

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
            cpp_files.append(line)
    
    return cpp_files

def compile_mytest():
    target_dir = subjects_dir / 'mytest'
    target_code = target_dir / 'a' / 'b' / 'mytest.c'
    cmd = [
        'clang', '-O0',
        '-fprofile-arcs', '-ftest-coverage', '-g',
        target_code, '-o', target_dir / 'a' / 'b' / 'mytest'
    ]
    res = sp.call(cmd, cwd=target_dir / 'a' / 'b', stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    if res != 0:
        print('compiling code failed: {}'.format(res))
        exit(1)

def compile_fuzzer(project_dir, dir_name):
    build_dir = project_dir / dir_name
    fuzzer = build_dir / 'jsoncpp_fuzzer'
    link_file = build_dir / 'src/lib_json/libjsoncpp.a'
    fuzz_dir = project_dir / 'src/test_lib_json'

    cmd = [
        clangPP, '-O0',
        '-fprofile-arcs', '-ftest-coverage', '-g',
        '-fno-omit-frame-pointer', '-gline-tables-only',
        '-DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION',
        '-fsanitize=address,undefined',
        '-fsanitize-address-use-after-scope',
        '-fsanitize=fuzzer-no-link',
        '-I../../include', '-fsanitize=fuzzer',
        './fuzz.cpp', '-o', fuzzer, link_file
    ]

    res = sp.call(cmd, cwd=fuzz_dir)
    if res != 0:
        print('compiling fuzzer failed: {}'.format(res))
        exit(1)

    print('>> compiled fuzzer')

def extract_line2function(project_path, cpp_files):
    preprocessed_dir = project_path / 'preprocessed'

    cmd = [extractor_exe]

    cnt = 0

    perFile_data = {}
    for file in cpp_files:
        file_path = Path(file)
        target_cpp = preprocessed_dir / file_path
        cmd.append(target_cpp)

        process = sp.Popen(
            cmd, stdout=sp.PIPE, stderr=sp.STDOUT,
            encoding='utf-8'
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
    mutation_name = sys.argv[1]
    template_name = sys.argv[2]

    # clean
    # clean_mytest()
    clean_json_build_dir(subjects_dir / template_name, only_pp=False)

    # get preprocessed code
    # build_mytest_pp()
    build_jsoncpp(subjects_dir / template_name, 'preprocessed', preprocessed=True)
    make_jsoncpp(subjects_dir / template_name, 'preprocessed')
    ii_files = get_ii_files(subjects_dir / template_name)
    cpp_files = change_ii_to_cpp(subjects_dir / template_name, ii_files)
    for cpp in cpp_files:
        print(cpp)
    perFile_line2method_data = extract_line2function(subjects_dir / template_name, cpp_files)
    write_line2function(subjects_dir / template_name, perFile_line2method_data, mutation_name)
    clean_json_build_dir(subjects_dir / template_name, only_pp=True)

    # compile code
    # compile_mytest()
    build_jsoncpp(subjects_dir / template_name, 'build')
    make_jsoncpp(subjects_dir / template_name, 'build')
    compile_fuzzer(subjects_dir / template_name, 'build')
