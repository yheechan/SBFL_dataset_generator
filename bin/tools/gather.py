#!/usr/bin/python3

import subprocess as sp
from pathlib import Path
import os
from utils import myHelper as hh
import pandas as pd

def copy_data(src_dir, dest_dir):
    hh.check_dir(dest_dir)

    summary_files = []

    for bug in bug_versions:
        dir_name = f'{project}-{bug}'
        dir_path = subjects_dir / dir_name
        data_dir = dir_path / 'data' / src_dir

        for filepath in data_dir.iterdir():
            file_name = filepath.name
            is_summary = True if file_name.split('.')[1] == 'rank' else False
            if is_summary:
                summary_files.append(filepath)
                continue
            sp.call(['cp', str(filepath), str(dest_dir)])
    
    if len(summary_files) != 0:
        df = pd.DataFrame()
        file_path = dest_dir / 'total.rank.summary.csv'
        # sort file_path by file name
        summary_files = sorted(summary_files, key=lambda x: x.name)
        for summary_file in summary_files:
            df = pd.concat([df, pd.read_csv(summary_file)], axis=0)
        df.to_csv(file_path, index=False)


if __name__ == "__main__":
    script_file_path = Path(os.path.realpath(__file__))
    tool_dir = script_file_path.parent
    bin_dir = tool_dir.parent
    main_dir = bin_dir.parent
    subjects_dir = main_dir / 'subjects'
    overall_dir = main_dir / 'overall'

    project = 'jsoncpp'
    bug_versions = []

    for project_path in subjects_dir.iterdir():
        project_name = project_path.name
        project = project_name.split('-')[0]
        bug = project_name.split('-')[1]

        bug_versions.append(bug)

    # 1. make overall directory
    hh.check_dir(overall_dir)

    # 2. Copy coincident data to overall
    coverage_dir = overall_dir / 'coverage'
    hh.check_dir(coverage_dir)
    copy_data('coverage/coincident', coverage_dir / 'coincident')

    # 2-1. Copy raw data to overall
    copy_data('coverage/raw', coverage_dir / 'raw')

    # 2-2. Copy summary data to overall
    copy_data('coverage/summary', coverage_dir / 'summary')

    # 3. Copy criteria data to overall
    copy_data('criteria', overall_dir / 'criteria')

    # 4. Copy spectra data to overall
    copy_data('spectra', overall_dir / 'spectra')

    # 5. Copy processed data to overall
    copy_data('processed', overall_dir / 'processed')

    # 6. Copy ranked data to overall
    copy_data('ranked-line', overall_dir / 'ranked-line')
    # copy_data('ranked-function', overall_dir / 'ranked-function')

    # 7. Copy line2function data to overall
    copy_data('line2function', overall_dir / 'line2function')

    #8. Copy ranked summary data to overall
    copy_data('summary', overall_dir / 'summary')
