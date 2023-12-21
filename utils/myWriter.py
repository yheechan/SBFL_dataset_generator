import subprocess as sp
from pathlib import Path
import os
import csv
from . import myHelper as hh

script_path = Path(os.path.realpath(__file__))
util_dir = script_path.parent
bin_dir = util_dir.parent
main_dir = bin_dir.parent
test_dir = main_dir / 'build-1/src/test_lib_json'
data_dir = main_dir / 'data'
coverage_dir = main_dir / 'coverage'
spectra_dir = data_dir / 'spectra'
tc_list_file = coverage_dir / 'tc-list.txt'
cov_pretty_dir = coverage_dir / 'cov_pretty'
html_dir = coverage_dir / 'html'
summary_dir = coverage_dir / 'summary'

def write_spectra_data_to_csv(spectra_data_per_file: dict):
    hh.check_dir(data_dir)
    hh.check_dir(spectra_dir)

    for file in spectra_data_per_file.keys():
        file_name = file.replace('/', '.') + '.csv'
        row_data = spectra_data_per_file[file]['row_data']
        col_data = spectra_data_per_file[file]['col_data']

        file = spectra_dir / file_name
        with open(file, 'w') as fp:
            cw = csv.writer(fp)
            cw.writerow(col_data)
            cw.writerows(row_data)

def write_test_cases_list_to_txt(tc_list: list, pp=False):
    hh.check_dir(data_dir)
    file = data_dir / 'tc-list.txt'
    with open(file, 'w') as fp:
        for tc in tc_list.keys():
            line = '{}-{}: {}'.format(
                tc, tc_list[tc]['type'],
                tc_list[tc]['name']
            )
            fp.write(line+'\n')

            if pp:
                print(line)

def write_TC_on_criterion_to_csv(criterion_data: dict):
    hh.check_dir(data_dir)
    file = data_dir / 'TC.criterion.csv'

    col_data = criterion_data['col_data']
    row_data = criterion_data['row_data']

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)

def write_criterion_stat_results(cd, tot):
    hh.check_dir(data_dir)
    file = data_dir / 'criterion_stats.csv'

    xF_file = cd['xx_fail_file']
    nF_file = tot-xF_file
    xF_func = cd['xx_fail_func']
    nF_func = tot-xF_func
    xF_line = cd['xx_fail_line']
    nF_line = tot-xF_line

    col_data = ['criterion', 'executes', 'not-executes', 'total']
    row_data = [
        ['buggy-file', xF_file, nF_file, tot],
        ['buggy-func', xF_func, nF_func, tot],
        ['buggy-line', xF_line, nF_line, tot]
    ]

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)
