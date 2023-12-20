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
