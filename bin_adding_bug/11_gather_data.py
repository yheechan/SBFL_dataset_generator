#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
mutations_output_dir = main_dir / 'mutations'
bugs_dir = main_dir / 'bugs'

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()

def copy_data(src_dir, dest_dir, bug_versions):
    check_dir(dest_dir)

    # summary_files = []

    for bug in bug_versions:
        # dir_name = f'{project}-{bug}'
        # dir_path = subjects_dir / dir_name
        # data_dir = dir_path / 'data' / src_dir
        data_dir = bug / 'data' / src_dir

        for filepath in data_dir.iterdir():
            # file_name = filepath.name
            # is_summary = True if file_name.split('.')[1] == 'rank' else False
            # if is_summary:
            #     summary_files.append(filepath)
            #     continue
            sp.call(['cp', str(filepath), str(dest_dir)])
    
    # if len(summary_files) != 0:
    #     df = pd.DataFrame()
    #     file_path = dest_dir / 'total.rank.summary.csv'
    #     # sort file_path by file name
    #     summary_files = sorted(summary_files, key=lambda x: x.name)
    #     for summary_file in summary_files:
    #         df = pd.concat([df, pd.read_csv(summary_file)], axis=0)
    #     df.to_csv(file_path, index=False)

if __name__ == "__main__":
    
    versions = []
    for machines in sorted(bugs_dir.iterdir()):
        for target in sorted(machines.iterdir()):
            versions.append(target)
    print('total bugs: {}'.format(len(versions)))
    
    overall_dir = main_dir / 'overall'
    check_dir(overall_dir)
    
    # make coverage directory
    coverage_dir = overall_dir / 'coverage'
    check_dir(coverage_dir)
    
    # copy coverage data
    copy_data('coverage/raw', coverage_dir / 'raw', versions)

    # copy summary data
    copy_data('coverage/summary', coverage_dir / 'summary', versions)

    # copy spectra data
    copy_data('spectra', overall_dir / 'spectra', versions)

    # copy processed data
    copy_data('processed', overall_dir / 'processed', versions)

    # copy ranked-line
    copy_data('ranked-line', overall_dir / 'ranked-line', versions)

