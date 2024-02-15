#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import sys

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'
mutations_dir = main_dir / 'mutations'

apply_mutation = bin_dir / '1_apply_mutation.py'
compile_code = bin_dir / '2_compile.py'
line2method = bin_dir / '3_line2method.py'
run_tc = bin_dir / '4_run_testcases.py'
postprocess_cov = bin_dir / '5_postprocess_cov.py'
measure_spectrum = bin_dir / '6_measure_spectrum.py'
save_data = bin_dir / '7_save_data.py'

if __name__ == "__main__":
    
    mutation_info = ''
    for file in mutations_dir.iterdir():
        for mutation in file.iterdir():
            if mutation.name.split('.')[-1] == 'csv':
                mutation_info = mutation
                break


    ###############################
    # 1. apply mutation one by one
    for file in mutations_dir.iterdir():
        mutation_info = ''
        for mutation in file.iterdir():
            if mutation.name.split('.')[-1] == 'csv':
                mutation_info = mutation
                break
        if mutation_info == '':
            print('[SKIP] mutation_info not found for {}'.format(file))
            continue

        cnt = 0
        # for single mutation
        for mutation in file.iterdir():
            if mutation.name.split('.')[-1] == 'csv':
                continue

            mutation_name = mutation.name
            mutation_id = mutation_name.split('.')[1]

            mutation_file_path_str = mutation.parent.name
            target_src_file_name = mutation_file_path_str.split('-')[-1]
            target_src_file_path = '/'.join(mutation_file_path_str.split('-')[:-1])
            
            cmd = [
                apply_mutation, mutation,
                mutation_name, mutation_id,
                mutation_file_path_str, target_src_file_name, target_src_file_path
            ]
            res = sp.call(cmd, cwd=bin_dir)
            print('applying mutation: {}\n'.format(res))

            #################
            # 2. compile code
            if target_src_file_name != 'mytest.c':
                break

            cmd = [compile_code]
            res = sp.call(cmd, cwd=bin_dir, stdout=sp.DEVNULL, stderr=sp.STDOUT)
            # if compile error move to step 1
            if res != 0:
                print('compiling code failed: {}'.format(res))
                continue


            #################################
            # 3. retreive line2method mapping
            cmd = [line2method, mutation_name]
            res = sp.call(cmd, cwd=bin_dir)
            if res != 0:
                print('line2method failed: {}'.format(res))
                continue


            ###################
            # 4. run test cases
            cmd = [run_tc, mutation_name, mutation_info, mutation_file_path_str]
            res = sp.call(cmd, cwd=bin_dir)
            if res == 111:
                print('[{}] has no bug on this version: {}'.format(res, mutation_name))
                continue
            # elif res != 0:
            #     print('line2method failed: {}'.format(res))
            #     continue
            print('[{}] this version has bug: {}'.format(res, mutation_name))


            ###############################
            # 5. post-process coverage data
            cmd = [postprocess_cov, mutation_name, mutation_info, mutation_file_path_str]
            res = sp.call(cmd, cwd=bin_dir)
            if res != 0:
                print('post-process coverage data failed: {}'.format(res))
                continue

            ###############################
            # 6. measure spectrum (formula)
            cmd = [measure_spectrum, mutation_name, mutation_info, mutation_file_path_str]
            res = sp.call(cmd, cwd=bin_dir)
            if res != 0:
                print('measure spectrum failed: {}'.format(res))
                continue
            
            ###############
            # 7. save (record) data
            cmd = [save_data, mutation_name, mutation_info, mutation_file_path_str]
            res = sp.call(cmd, cwd=bin_dir)
            if res != 0:
                print('save data failed: {}'.format(res))
                continue

            # if cnt == 0:
            #     break
            # cnt += 1

