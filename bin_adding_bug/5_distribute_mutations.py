#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
mutations_output_dir = main_dir / 'mutations'

if __name__ == "__main__":
    # get list of line in avail_machine_file
    avail_machine_file = open('available_machine.txt', 'r')
    lines = avail_machine_file.readlines()
    
    available_machine_list = []
    for line in lines:
        info = line.strip().split(':')
        if info[1] == 'ok':
            available_machine_list.append(info[0])
    print('available machine total: {}'.format(len(available_machine_list)))

    # count number of files (mutations) to distribute
    # dict that contains key as file and value as number of mutations
    mutations_dict = {}
    total_cnt = 0
    mutation_info_dict = {}
    for file_dir in mutations_output_dir.iterdir():
        cnt = 0
        if file_dir not in mutations_dict:
            mutations_dict[file_dir] = []
        
        # change following code so that file_dir.iterdir() show with sorted order by file_dir.name
        for mutation in sorted(file_dir.iterdir(), key=lambda x: x.name):
            # save the mutation info (csv file)
            if mutation.name.split('.')[-1] == 'csv':
                file_name = file_dir.name
                if file_name not in mutation_info_dict:
                    mutation_info_dict[file_name] = mutation
                continue
            mutations_dict[file_dir].append(mutation)
            cnt += 1
            total_cnt += 1
    print('total mutations: {}'.format(total_cnt))
    for key in mutations_dict:
        print('{}: {}'.format(key.name, len(mutations_dict[key])))
    
    # assigns equall amount of mutations to each machine
    machine2mutations = {}
    curr_machine = 0
    mutation_cnt = 0
    per_machine = total_cnt//len(available_machine_list)
    print('per machine: {}'.format(per_machine))

    for file in mutations_dict.keys():
        file_name = file.name
        for mutation in mutations_dict[file]:
            machine = available_machine_list[curr_machine]
            if not machine in machine2mutations:
                machine2mutations[machine] = []

            machine2mutations[machine].append((file_name, mutation))
            if mutation_cnt == -1:
                curr_machine += 1
                if curr_machine == len(available_machine_list):
                    curr_machine = 0
                continue
            
            mutation_cnt += 1

            if mutation_cnt == (total_cnt//len(available_machine_list)):
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


    bash_file = open('5_distribute_mutations.sh', 'w')
    bash_file.write('date\n')

    # make mutation directory in machines
    # with all the directory for each file
    # and send the assigned files
    cnt = 0
    for machine in available_machine_list:
        cmd = 'ssh {} \" cd SBFL_dataset_generator && mkdir mutations && cd mutations '.format(machine)
        for file in mutations_dict.keys():
            file_name = file.name
            cmd += '&& mkdir {} \"'.format(file_name)
        cmd += '\n'
        bash_file.write(cmd)

        if cnt % 5 == 0:
            bash_file.write("sleep 1s\n")
        cnt  += 1

        for csv_info in mutation_info_dict:
            file_name = csv_info
            mutation_file = mutation_info_dict[csv_info]
            cmd = 'scp {} {}:/home/yangheechan/SBFL_dataset_generator/mutations/{}/ & \n'.format(mutation_file, machine, file_name)
            bash_file.write(cmd)
            if cnt % 5 == 0:
                bash_file.write("sleep 1s\n")
            cnt  += 1
        
        # send mutations to the machine
        for mutation in machine2mutations[machine]:
            file_name = mutation[0]
            mutation_file = mutation[1]
            cmd = 'scp {} {}:/home/yangheechan/SBFL_dataset_generator/mutations/{}/ & \n'.format(mutation_file, machine, file_name)
            bash_file.write(cmd)
            if cnt % 5 == 0:
                bash_file.write("sleep 1s\n")
            cnt  += 1

    
    bash_file.write('echo ssh done, waiting...\n')
    bash_file.write('date\n')
    bash_file.write('wait\n')
    bash_file.write('date\n')
    
    cmd = ['chmod', '+x', '5_distribute_mutations.sh']
    res = sp.call(cmd, cwd=bin_dir)
