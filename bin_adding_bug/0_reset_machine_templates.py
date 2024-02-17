#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
make_template_script = bin_dir / '1_make_template.py'

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
    
    bash_file = open('0_reset_machine_templates.sh', 'w')
    bash_file.write('date\n')

    cnt = 0
    for machine in available_machine_list:
        command = 'ssh {} \"cd SBFL_dataset_generator && '.format(machine)
        # command += 'rm -rf subjects && cd bin_adding_bug && python3 1_make_template.py\" \n'
        command += 'rm -rf subjects\" \n'
        bash_file.write(command)

        bash_file.write("sleep 1s\n")
        bash_file.write("wait\n")

        command = 'ssh {} \"cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.{}.0 2>&1\" & \n'.format(
            machine,machine
        )
        bash_file.write(command)

        if cnt % 3 == 0:
            bash_file.write("sleep 8s\n")
            bash_file.write("wait\n")
        cnt += 1
    
    bash_file.write('echo ssh done, waiting...\n')
    bash_file.write('date\n')
    bash_file.write('wait\n')
    bash_file.write('date\n')
        
    cmd = ['chmod', '+x', '0_reset_machine_templates.sh']
    res = sp.call(cmd, cwd=bin_dir)
