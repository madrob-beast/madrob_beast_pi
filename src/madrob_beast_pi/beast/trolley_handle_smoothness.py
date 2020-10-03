#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime
import pandas as pd


def performance_indicator(preprocessed_filenames_dict, _, output_dir, start_time):

    wrench_df = pd.read_csv(preprocessed_filenames_dict['wrench'])

    force_delta_sum = 0

    for index, row in wrench_df.iterrows():
        if index > 0:
            force_delta_sum += abs(row['force_x'] - wrench_df.loc[index-1, 'force_x']) / (row['time'] - wrench_df.loc[index-1, 'time'])

    smoothness = 100. / (force_delta_sum/len(wrench_df))  # Higher smoothness = lower force deltas

    # Write result yaml file
    filepath = path.join(output_dir, 'trolley_handle_smoothness.yaml')
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': float(smoothness),
        }, result_file, default_flow_style=False)

    return 0


def run_pi(wrench_path, output_folder_path):
    return performance_indicator({'wrench': wrench_path}, None, output_folder_path, datetime.now())


if __name__ == '__main__':
    arg_len = 3
    script_name = 'trolley_handle_smoothness'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py wrench.csv output_dir".format(script_name=script_name)
        exit(-1)

    wrench_path, output_folder_path = argv[1:]
    performance_indicator({'wrench': wrench_path}, None, output_folder_path, datetime.now())
