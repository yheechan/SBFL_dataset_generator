#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import random

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
mutations_output_dir = main_dir / 'mutations'

if __name__ == "__main__":
    # 1. GET NUMBER OF AVAILABLE MACHINES
    avail_machine_file = open('available_machine.txt', 'r')
    lines = avail_machine_file.readlines()
    
    available_machine_list = []
    for line in lines:
        info = line.strip().split(':')
        if info[1] == 'ok':
            available_machine_list.append(info[0])
    print('available machine total: {}'.format(len(available_machine_list)))

    # 2. COLLECT BUGGY MUTATIONS TO
    # BUGGY_MUTATION_DICT PER MUTATION_PATH_ORIGIN
    buggy_mutation_dir = main_dir / 'buggy_mutations'
    buggy_mutation_dict = {}
    total_buggy_mutation = 0
    for file in buggy_mutation_dir.iterdir():
        for mutation in file.iterdir():
            list_file = open(mutation, 'r')
            lines = list_file.readlines()
            for line in lines:
                line = line.strip()
                info = line.split('##')
                mutation_id = info[0]
                mutation_path_origin = info[1]

                if mutation_path_origin not in buggy_mutation_dict:
                    buggy_mutation_dict[mutation_path_origin] = []
                buggy_mutation_dict[mutation_path_origin].append(mutation_id)
                total_buggy_mutation += 1

    print('total buggy mutation: {}'.format(total_buggy_mutation))
    for key in buggy_mutation_dict:
        print('\t{}: {}'.format(key, len(buggy_mutation_dict[key])))

    # 3. INITIATE FILE TO SAVE SELECTED MUTANTS
    selected_file = main_dir / 'selected_mutation.txt'
    if selected_file.exists():
        selected_file.unlink()
    if not selected_file.exists():
        selected_file.touch()
    selected_file = open(selected_file, 'a')
    
    # 4. DISTRIBUTE EQUALL AMOUNT OF MUTANTS PER FILE
    selecting_amount = 160
    select_cnt = int(selecting_amount // len(buggy_mutation_dict))
    print('selecting amount: {}'.format(selecting_amount))
    print('selecting count per file: {}'.format(select_cnt))

    # 5. SELECT MUTANTS PER FILE
    selected_per_file = {}
    old_selected_per_file = {}
    old_selected_on_line = {}
    for file in buggy_mutation_dict:
        selected_per_file[file] = []
        old_selected_per_file[file] = []
        old_selected_on_line[file] = []

        # GET MUTANT INFO DB TO MATCH MUTANT TO SOURCE CODE LINE
        file_name_info = file.split('-')[-1].split('.')
        csv_file_name = file_name_info[0] + '_mut_db.csv'
        info_path = main_dir / 'mutations' / file / csv_file_name
        assert info_path.exists()
        db_file = open(info_path, 'r')
        db_lines = db_file.readlines()

        # shuffle buggy_mutation_dict[file] which is a list of mutation_id
        random.shuffle(buggy_mutation_dict[file])
        
        lineNum2mutations = {}
        total_mutation = len(buggy_mutation_dict[file])
        curr_cnt = 0
        # SAVE MUTANTS ON ITS LINE
        # KEY: LINE, VALUE: LIST OF MUTANTS ON THE LINE
        for mutation_id in buggy_mutation_dict[file]:
            curr_cnt += 1
            # print('current: {}/{}'.format(curr_cnt, total_mutation))

            # get mutation info from db
            for db_line in db_lines:
                db_line = db_line.strip()
                db_info = db_line.split(',')

                # FOUND MUTANT INFO IN DB
                if mutation_id == db_info[0]:
                    start_line = int(db_info[2])
                    if start_line not in lineNum2mutations:
                        lineNum2mutations[start_line] = []
                    lineNum2mutations[start_line].append(mutation_id)
        
        past_selected_mutations = main_dir / 'selected_mutation-v1.txt'
        past_list = open(past_selected_mutations, 'r')
        past_lines = past_list.readlines()
        for line in past_lines:
            line = line.strip()
            info = line.split(',')
            old_mutant_id = info[0]
            old_line = str(info[1])
            old_selected_per_file[file].append(old_mutant_id)
            old_selected_on_line[file].append(old_line)




        cnt = 0
        flag = 1
        completed = 0
        # FOR THIS FILE, SELECT MUTANTS THAT ARE ON THE SAME LINE
        while True:
            turn = 0
            for line in lineNum2mutations:
                if turn >= len(lineNum2mutations[line]):
                    continue
                if lineNum2mutations[line][turn] in old_selected_per_file[file]:
                    continue
                if str(line) in old_selected_on_line[file]:
                    continue
                flag = 0

                selected_per_file[file].append(lineNum2mutations[line][turn])
                data = '{},{},{}\n'.format(lineNum2mutations[line][turn], line, turn+1)
                selected_file.write(data)

                cnt += 1
                if cnt == select_cnt:
                    completed = 1
                    break
            if completed == 1: break
            if flag == 1: break
            turn += 1

    total_amount = 0
    amount = 0
    for key in selected_per_file:
        amount = len(selected_per_file[key])
        total_amount += amount
        print('{}: {}'.format(key, amount))
    print('total: {}'.format(total_amount))
        
        
    # count number of files (mutations) to distribute
    # dict that contains key as file and value as number of mutations
    mutation_info_dict = {}
    for file_dir in mutations_output_dir.iterdir():
        # change following code so that file_dir.iterdir() show with sorted order by file_dir.name
        for mutation in sorted(file_dir.iterdir(), key=lambda x: x.name):
            # save the mutation info (csv file)
            if mutation.name.split('.')[-1] == 'csv':
                file_name = file_dir.name
                if file_name not in mutation_info_dict:
                    mutation_info_dict[file_name] = mutation
                    break
    
    # 6. assigns equall amount of mutations to each machine
    machine2mutations = {}
    curr_machine = 0
    mutation_cnt = 0
    per_machine = selecting_amount//len(available_machine_list)
    print('per machine: {}'.format(per_machine))

    for key in selected_per_file.keys():
        file = main_dir / 'mutations' / key
        file_name = file.name
        for mutation in selected_per_file[key]:
            machine = available_machine_list[curr_machine]
            if not machine in machine2mutations:
                machine2mutations[machine] = []

            mutation = file / mutation
            machine2mutations[machine].append((file_name, mutation))
            if mutation_cnt == -1:
                curr_machine += 1
                if curr_machine == len(available_machine_list):
                    curr_machine = 0
                continue
            
            mutation_cnt += 1

            if mutation_cnt == per_machine:
                curr_machine += 1
                mutation_cnt = 0
                if curr_machine == len(available_machine_list):
                    curr_machine = 0
                    mutation_cnt = -1
    
    # show number of mutations assigned to each machine
    total_assigned = 0
    for machine in machine2mutations:
        print('{}: {}'.format(machine, len(machine2mutations[machine])))
        total_assigned += len(machine2mutations[machine])
    print('total assigned: {}'.format(total_assigned))


    bash_file = open('8_select_mutation_and_send.sh', 'w')
    bash_file.write('date\n')

    # make mutation directory in machines
    # with all the directory for each file
    # and send the assigned files
    cnt = 0
    laps = 50
    cores = 8
    for machine in available_machine_list:
        cmd = 'ssh {} \" cd SBFL_dataset_generator && mkdir mutations && cd mutations '.format(machine)
        for core_n in range(cores):
            for key in selected_per_file.keys():
                file = main_dir / 'mutations' / key
                file_name = file.name
                cmd += '&& mkdir -p core{}/{} '.format(core_n, file_name)
        cmd += '\" \n'
        bash_file.write(cmd)
        bash_file.write("sleep 0.5s\n")
        bash_file.write("wait\n")

        # if cnt % 5 == 0:
        #     bash_file.write("sleep 0.5s\n")
        bash_file.write("wait\n")
        # cnt  += 1

        for core_n in range(cores):
            for csv_info in mutation_info_dict:
                file_name = csv_info
                mutation_file = mutation_info_dict[csv_info]
                cmd = 'scp {} {}:/home/yangheechan/SBFL_dataset_generator/mutations/core{}/{}/ & \n'.format(
                    mutation_file, machine, core_n, file_name
                )
                bash_file.write(cmd)
                if cnt % laps == 0:
                    bash_file.write("sleep 0.5s\n")
                    bash_file.write("wait\n")
                cnt  += 1
        
        # send mutations to the machine
        saving = 0
        for mutation in machine2mutations[machine]:
            file_name = mutation[0]
            mutation_file = mutation[1]
            curr_core = saving % cores
            cmd = 'scp {} {}:/home/yangheechan/SBFL_dataset_generator/mutations/core{}/{} & \n'.format(
                mutation_file, machine, curr_core, file_name
            )
            bash_file.write(cmd)
            saving += 1
            if cnt % laps == 0:
                bash_file.write("sleep 0.5s\n")
                bash_file.write("wait\n")
            cnt  += 1

    
    bash_file.write('echo ssh done, waiting...\n')
    bash_file.write('date\n')
    bash_file.write('wait\n')
    bash_file.write('date\n')
    
    cmd = ['chmod', '+x', '8_select_mutation_and_send.sh']
    res = sp.call(cmd, cwd=bin_dir)
