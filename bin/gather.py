#!/usr/bin/python3

import subprocess as sp
from pathlib import Path
import os
from utils import myHelper as hh

def copy_data(src_dir, dest_dir):
    hh.check_dir(dest_dir)

    for bug in bug_versions:
        dir_name = f'{project}-{bug}'
        dir_path = subjects_dir / dir_name
        data_dir = dir_path / 'data' / src_dir

        for filepath in data_dir.iterdir():
            sp.call(['cp', str(filepath), str(dest_dir)])

if __name__ == "__main__":
    script_file_path = Path(os.path.realpath(__file__))
    bin_dir = script_file_path.parent
    main_dir = bin_dir.parent
    subjects_dir = main_dir / 'subjects'
    overall_dir = main_dir / 'overall'

    project = 'jsoncpp'
    bug_versions = ['bug1', 'bug2', 'bug3', 'bug4']

    # 1. make overall directory
    hh.check_dir(overall_dir)

    # 2. Copy coincident data to overall
    copy_data('coverage/coincident', overall_dir / 'coincident')

    # 3. Copy criteria data to overall
    copy_data('criteria', overall_dir / 'criteria')

    # 4. Copy spectra data to overall
    copy_data('spectra', overall_dir / 'spectra')

    # 5. Copy processed data to overall
    copy_data('processed', overall_dir / 'processed')

    # 6. Copy ranked data to overall
    copy_data('ranked', overall_dir / 'ranked')

    # 7. Copy line2function data to overall
    copy_data('line2function', overall_dir / 'line2function')
