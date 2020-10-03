#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, _, output_dir, start_time):

    time_to_handle = 'TIMEOUT'

    events_df = pd.read_csv(preprocessed_filenames_dict['events'], skipinitialspace=True)

    # Check if there's a 'handle_is_touched' event
    handle_is_touched_events = events_df.loc[events_df['event'] == 'handle_is_touched']
    if len(handle_is_touched_events) > 0:
        handle_is_touched = handle_is_touched_events.iloc[0]

        time_to_handle = float(handle_is_touched['time']) - float(events_df.loc[events_df['event'] == 'benchmark_start']['time'])

    # Write result yaml file
    filepath = path.join(output_dir, 'time_to_handle.yaml')
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': time_to_handle,
        }, result_file, default_flow_style=False)


def run_pi(events_path, output_folder_path):
    performance_indicator({'events': events_path}, None, output_folder_path, datetime.now())
    return 0


if __name__ == '__main__':
    arg_len = 3
    script_name = 'time_to_handle'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py events.csv output_dir".format(script_name=script_name)
        exit(-1)

    events_path, output_folder_path = argv[1:]
    run_pi(events_path, output_folder_path)