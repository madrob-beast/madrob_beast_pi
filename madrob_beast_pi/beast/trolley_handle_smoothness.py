#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, _, output_dir, start_time):

    force_df = pd.read_csv(preprocessed_filenames_dict['handle_force'])

    force_delta_sum = 0

    for index, row in force_df.iterrows():
        if index > 0:
            force_delta_sum += abs(row['handle_force'] - force_df.loc[index-1, 'handle_force']) / (row['timestamp'] - force_df.loc[index-1, 'timestamp'])

    smoothness = 10000 / (force_delta_sum/len(force_df)) # Higher smoothness = lower force deltas

    # Write result yaml file
    filepath = path.join(output_dir, 'trolley_handle_smoothness_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({'trolley_handle_smoothness': float(smoothness)}, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 3
    script_name = 'trolley_handle_smoothness'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py handle_force.csv output_dir".format(script_name=script_name)
        exit(-1)

    handle_force_path, output_folder_path = argv[1:]
    performance_indicator({'handle_force': handle_force_path}, None, output_folder_path, datetime.now())
