#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, condition, output_dir, start_time):

    passage_time = 'TIMEOUT'

    events_df = pd.read_csv(preprocessed_filenames_dict['event'], skipinitialspace=True)

    # Check if there's a 'door_close' event
    door_closes_events = events_df.loc[events_df['event'] == 'door_closes']
    if len(door_closes_events) > 0:
        last_door_close = door_closes_events.iloc[-1]

        # Finally, check if the 'handle_is_touched' event exists
        handle_is_touched_events = events_df.loc[events_df['event'] == 'handle_is_touched']
        if len(handle_is_touched_events) > 0:
            first_handle_touch = handle_is_touched_events.iloc[0]

            passage_time = float(last_door_close['time']) - float(first_handle_touch['time'])

    # Write result yaml file
    filepath = path.join(output_dir, 'passage_time.yaml')
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': passage_time,
        }, result_file, default_flow_style=False)


def run_pi(event_path, condition_path, output_folder_path):
    with open(condition_path, 'r') as condition_file:
        condition_dict = yaml.safe_load(condition_file)

    performance_indicator({'event': event_path}, condition_dict, output_folder_path, datetime.now())
    return 0


if __name__ == '__main__':
    arg_len = 4
    script_name = 'passage_time'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py event.csv condition.yaml output_dir".format(script_name=script_name)
        exit(-1)

    event_path, condition_path, output_folder_path = argv[1:]

    run_pi(event_path, condition_path, output_folder_path)