#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
project_dir = bin_dir.parent

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
    
    bash_file = open('2_send_dataset_generating_tool.sh', 'w')
    bash_file.write('date\n')

    cnt = 0
    for machine in available_machine_list:
        command = 'scp -r {} {}:/home/yangheechan & \n'.format(project_dir, machine)
        bash_file.write(command)

        if cnt % 5 == 0:
            bash_file.write("sleep 0.5s\n")
            bash_file.write("wait\n")
        cnt += 1
    
    bash_file.write('echo ssh done, waiting...\n')
    bash_file.write('date\n')
    bash_file.write('wait\n')
    bash_file.write('date\n')

    cmd = ['chmod', '+x', '2_send_dataset_generating_tool.sh']
    res = sp.call(cmd, cwd=bin_dir)