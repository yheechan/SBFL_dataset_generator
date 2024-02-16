#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
mutations_output_dir = main_dir / 'mutations'
# bugs_dir = main_dir / 'bugs'

if __name__ == "__main__":
    # if not bugs_dir.exists():
    #     bugs_dir.mkdir()
    buggy_mutations_dir = main_dir / 'buggy_mutations'
    if not buggy_mutations_dir.exists():
        buggy_mutations_dir.mkdir()
    
    # get list of line in avail_machine_file
    avail_machine_file = open('available_machine.txt', 'r')
    lines = avail_machine_file.readlines()
    
    available_machine_list = []
    for line in lines:
        info = line.strip().split(':')
        if info[1] == 'ok':
            available_machine_list.append(info[0])
    print('available machine total: {}'.format(len(available_machine_list)))
    
    bash_file = open('7_retreive_buggy_mutations.sh', 'w')
    bash_file.write('date\n')

    cnt = 0
    for machine in available_machine_list:
        # command = 'scp -r {}:/home/yangheechan/SBFL_dataset_generator/bugs {}/{} & \n'.format(machine, bugs_dir, machine)
        command = 'scp -r {}:/home/yangheechan/SBFL_dataset_generator/buggy_mutations/ {}/{} & \n'.format(machine, buggy_mutations_dir, machine)
        bash_file.write(command)

        if cnt % 5 == 0:
            bash_file.write("sleep 0.5s\n")
            bash_file.write("wait\n")
        cnt += 1
    
    bash_file.write('echo ssh done, waiting...\n')
    bash_file.write('date\n')
    bash_file.write('wait\n')
    bash_file.write('date\n')

    cmd = ['chmod', '+x', '7_retreive_buggy_mutations.sh']
    res = sp.call(cmd, cwd=bin_dir)
