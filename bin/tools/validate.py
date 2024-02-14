#!/usr/bin/python3

import subprocess as sp
from pathlib import Path
import os
import argparse

import pandas as pd

script_file_path = Path(os.path.realpath(__file__))
tools_dir = script_file_path.parent
bin_dir = tools_dir.parent
project_home = bin_dir.parent
overall_dir = project_home / 'overall'

rankedFunctions = overall_dir / 'ranked-function'
rankedLines = overall_dir / 'ranked-line'

versions = ['bug1', 'bug2', 'bug3', 'bug4']

def validate_broken_row():
    for version in versions:
        print('\nvalidating broken lines for version: {}'.format(version))

        # print('validating broken row for ranked function')
        # for file in rankedFunctions.iterdir():
        #     file_name = file.name
        #     file_version = file_name.split('.')[0]
        #     file_type = file_name.split('.')[1]

        #     if file_type == 'rank':
        #         continue

        #     if version == file_version:
        #         fp = open(file, 'r')
        #         lines = fp.readlines()
        #         out = pd.read_csv(file)
        #         # assert all value in all columns of all rows are not null
        #         assert out.isnull().values.any() == False
        #         print('\tno broken line for file: {}'.format(file_name))

        print('validating broken row for ranked line')
        for file in rankedLines.iterdir():
            file_name = file.name
            file_version = file_name.split('.')[0]
            file_type = file_name.split('.')[1]

            if file_type == 'rank':
                continue

            if version == file_version:
                fp = open(file, 'r')
                lines = fp.readlines()
                out = pd.read_csv(file)
                
                # assert all value in all columns of all rows are not null
                assert out.isnull().values.any() == False
                print('\tno broken line for file: {}'.format(file_name))

def validate_row_count():
    for version in versions:
        print('\nvalidating line count for version: {}'.format(version))

        # counts = []

        # print('validating line count for ranked function')
        # for file in rankedFunctions.iterdir():
        #     file_name = file.name
        #     file_version = file_name.split('.')[0]
        #     file_type = file_name.split('.')[1]

        #     if file_type == 'rank':
        #         continue

        #     if version == file_version:
        #         fp = open(file, 'r')
        #         lines = fp.readlines()
        #         counts.append(len(lines))
        #         print('\tline count for file: {} is {}'.format(file_name, len(lines)))
        
        # # assert if all the number inside counts list equall each other
        # assert counts[1:] == counts[:-1], 'line count for version {} is not equal'.format(version)

        counts = []

        print('validating line count for ranked line')
        for file in rankedLines.iterdir():
            file_name = file.name
            file_version = file_name.split('.')[0]
            file_type = file_name.split('.')[1]

            if file_type == 'rank':
                continue

            if version == file_version:
                fp = open(file, 'r')
                lines = fp.readlines()
                counts.append(len(lines))
                print('\tline count for file: {} is {}'.format(file_name, len(lines)))
        
        # assert if all the number inside counts list equall each other
        assert counts[1:] == counts[:-1], 'line count for version {} is not equal'.format(version)

# def validate_spectrum_data():
#     for version in versions:
#         print('validating spectrum data for version: {}'.format(version))

#         shapes = []
#         df = pd.DataFrame()
#         for file in rankedFunctions.iterdir():
#             file_name = file.name
#             file_version = file_name.split('.')[0]
#             file_type = file_name.split('.')[1]

#             if file_type == 'rank':
#                 continue

#             if version == file_version:
#                 out = pd.read_csv(file)

#                 # drop column 'Rank'
#                 out = out.drop(columns=['Rank'])
#                 shapes.append(out.shape)

#                 df = pd.concat([df, out], axis=0)

#         # write to csv file
#         df.to_csv('{}-ranked-function.csv'.format(version), index=False)
#         print(df.shape)
#         df = df.drop_duplicates()
#         print(df.shape)
        
#         print(shapes)

# def read_duplicates():
#     for version in versions:
#         print('reading duplicates for version: {}'.format(version))

#         df = pd.read_csv('{}-ranked-function.csv'.format(version))
#         duplicate = df[df.duplicated()]
#         df = df.drop_duplicates()
#         # write to csv file
#         duplicate.to_csv('{}-ranked-function-duplicates.csv'.format(version))
#         print(duplicate.shape)
        
def edit():
    # rankedLines
    rankedlines_upt = overall_dir / 'ranked-line-upt'
    if not rankedlines_upt.exists():
        rankedlines_upt.mkdir()
    
    print('validating broken row for ranked line')
    for version in versions:
        for file in rankedLines.iterdir():
            file_name = file.name
            file_version = file_name.split('.')[0]
            file_type = file_name.split('.')[1]

            if file_type == 'rank':
                continue

            if version == file_version:
                fp = open(file, 'r')
                lines = fp.readlines()
                out = pd.read_csv(file)
                out = out.drop(['Rank'], axis=1)

                file_path = rankedlines_upt / file_name
                out.to_csv(file_path, index=False)
                
                # assert all value in all columns of all rows are not null
                assert out.isnull().values.any() == False
                print('\tno broken line for file: {}'.format(file_name))
    pass

if __name__ == "__main__":
    validate_broken_row()
    validate_row_count()
    # edit()