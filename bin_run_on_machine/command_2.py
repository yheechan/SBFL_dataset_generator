#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import sys
import time

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'
# mutations_dir = main_dir / 'mutations'

apply_mutation = bin_dir / '1_apply_mutation.py'
compile_code = bin_dir / '2_compile.py'
line2method = bin_dir / '3_line2method.py'
run_tc = bin_dir / '4_run_testcases.py'
postprocess_cov = bin_dir / '5_postprocess_cov.py'
measure_spectrum = bin_dir / '6_measure_spectrum.py'
save_data = bin_dir / '7_save_data.py'
save_mutation = bin_dir / '8_save_mutation.py'

if __name__ == "__main__":
    # TIME_LIMIT = 5
    TIME_LIMIT = 60 * 5
    START_TIME = time.time()
    MYCORE = sys.argv[1]
    template_name = MYCORE
    
    m_dir = main_dir / 'mutations'
    mutations_dir = m_dir / template_name
    mutation_info = ''
    for file in mutations_dir.iterdir():
        for mutation in file.iterdir():
            if mutation.name.split('.')[-1] == 'csv':
                mutation_info = mutation
                break

    ###############################
    # 1. apply mutation one by one
    compile_error = 0
    run_but_no_bug = 0
    run_and_bug = 0
    file_count = 0
    for file in mutations_dir.iterdir():
        file_count += 1
        mutation_info = ''
        # when to skip
        for mutation in file.iterdir():
            if mutation.name.split('.')[-1] == 'csv':
                mutation_info = mutation
                break
        if mutation_info == '':
            print('{} : [SKIP] mutation_info not found for {}'.format(template_name, file))
            continue

        # remove data
        data_dir = subjects_dir / template_name / 'data'
        if data_dir.exists():
            cmd = ['rm', '-r', data_dir]
            sp.call(cmd, cwd=bin_dir)

        cnt = 0
        # for single mutation
        # get total count of file in file.iterdir()
        total_cnt = len(list(file.iterdir()))
        percentage = 0
        for mutation in file.iterdir():
            # print current percentage done for loop
            percentage += 1
            print('{} - {}/{} done on {} file'.format(template_name, percentage, total_cnt, file_count))
            if mutation.name.split('.')[-1] == 'csv':
                continue

            mutation_name = mutation.name
            mutation_id = mutation_name.split('.')[1]

            mutation_file_path_str = mutation.parent.name
            target_src_file_name = mutation_file_path_str.split('-')[-1]
            target_src_file_path = '/'.join(mutation_file_path_str.split('-')[:-1])

            print('{} [print info] - mutation_name: {}'.format(template_name, mutation_name))
            print('{} [print info] - mutation_id: {}'.format(template_name, mutation_id))
            print('{} [print info] - mutation_file_path_str: {}'.format(template_name, mutation_file_path_str))
            print('{} [print info] - target_src_file_name: {}'.format(template_name, target_src_file_name))
            print('{} [print info] - target_src_file_path: {}\n'.format(template_name, target_src_file_path))
            
            ###############################
            # 1. apply mutation one by one
            cmd = [
                apply_mutation, mutation,
                mutation_name, mutation_id,
                mutation_file_path_str, target_src_file_name, target_src_file_path,
                template_name
            ]
            print('{} - 1. start apply mutation'.format(template_name))
            res = sp.call(cmd, cwd=bin_dir, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            print('{} - 1. apply mutation: {}'.format(template_name, res))

            # ################
            # 2. compile code
            # if target_src_file_name != 'mytest.c':
            #     break

            cmd = [compile_code, mutation_name, template_name]
            print('{} - 2. start compile code'.format(template_name))
            res = sp.call(cmd, cwd=bin_dir, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            # if compile error move to step 1
            if res != 0:
                print('{} - 2 compiling code failed: {}'.format(template_name, res))
                compile_error += 1
                print('{} - 2. compile error count: {}'.format(template_name, compile_error))
                continue
            print('{} - 2. compile code: {}'.format(template_name, res))


            #################################
            # 3. retreive line2method mapping
            # cmd = [line2method, mutation_name]
            # res = sp.call(cmd, cwd=bin_dir)
            # if res != 0:
            #     print('line2method failed: {}'.format(res))
            #     continue


            ###################
            # 4. run test cases
            print('{} - 3. start run test cases'.format(template_name))
            cmd = [run_tc, mutation_name, mutation_info, template_name, 'True']
            res = sp.call(cmd, cwd=bin_dir)
            if res == 111:
                print('{} - 3. [{}] has no bug on this version: {}'.format(template_name, res, mutation_name))
                run_but_no_bug += 1
                print('{} - 3. run but no bug count: {}'.format(template_name, run_but_no_bug))
                continue
            print('{} - 3. [{}] this version has bug: {}'.format(template_name, res, mutation_name))
            run_and_bug += 1
            print('{} - 3. run and bug count: {}'.format(template_name, run_and_bug))
            print('{} - 3. run test cases: {}'.format(template_name, res))


            # ###############################
            # # 5. post-process coverage data
            cmd = [postprocess_cov, mutation_name, mutation_info, template_name]
            print('{} - 4. start post-process coverage data'.format(template_name))
            res = sp.call(cmd, cwd=bin_dir)
            if res != 0:
                print('{} - 4. post-process coverage data failed: {}'.format(template_name, res))
                continue
            print('{} - 4. post-process coverage data: {}'.format(template_name, res))

            # ###############################
            # 6. measure spectrum (formula)
            cmd = [measure_spectrum, mutation_name, mutation_info, mutation_file_path_str, target_src_file_path, template_name]
            print('{} - 5. start measure spectrum'.format(template_name))
            res = sp.call(cmd, cwd=bin_dir)
            if res != 0:
                print('{} - 5. measure spectrum failed: {}'.format(template_name, res))
                continue
            print('{} - 5. measure spectrum: {}'.format(template_name, res))
            
            # ###############
            # 7. save (record) data
            cmd = [save_data, mutation_name, mutation_info, template_name]
            print('{} - 6. start save data'.format(template_name))
            res = sp.call(cmd, cwd=bin_dir)
            if res != 0:
                print('{} - save data failed: {}'.format(template_name, res))
                continue
            print('{} - 6. save data: {}'.format(template_name, res))

            # # 8. save mutation since it passes run test case with failing TC
            # cmd = [save_mutation, template_name, mutation_name, mutation_file_path_str]
            # print('{} - 4. save mutation'.format(template_name))
            # res = sp.call(cmd, cwd=bin_dir, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            # if res != 0:
            #     print('{} - 4. save mutation failed: {}'.format(template_name, res))
            #     continue
            # print('{} - 4. save mutation: {}'.format(template_name, res))

        #     if cnt == 0:
        #         break
        #     cnt += 1
        # break

    print('{} - compile_error cnt: {}'.format(template_name, compile_error))
    print('{} - run_but_no_bug cnt: {}'.format(template_name, run_but_no_bug))
    print('{} - run_and_bug cnt: {}'.format(template_name, run_and_bug))


