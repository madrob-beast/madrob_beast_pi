#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, _, output_dir, start_time):

    time_to_handle = 'TIMEOUT'

    events_df = pd.read_csv(preprocessed_filenames_dict['events_sequence'], skipinitialspace=True)

    # Check if there's a 'handle_is_touched' event
    handle_is_touched_events = events_df.loc[events_df['events_sequence'] == 'handle_is_touched']
    if len(handle_is_touched_events) > 0:
        handle_is_touched = handle_is_touched_events.iloc[0]

        time_to_handle = float(handle_is_touched['timestamp']) - float(events_df.loc[events_df['events_sequence'] == 'benchmark_start']['timestamp'])

    # Write result yaml file
    filepath = path.join(output_dir, 'time_to_handle_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({'time_to_handle': time_to_handle}, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 3
    script_name = 'time_to_handle'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py events_sequence.csv output_dir".format(script_name=script_name)
        exit(-1)

    events_sequence_path, output_folder_path = argv[1:]
    performance_indicator({'events_sequence': events_sequence_path}, None, output_folder_path, datetime.now())
