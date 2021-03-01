#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, condition, output_dir, start_time):

    events_df = pd.read_csv(preprocessed_filenames_dict['event'], skipinitialspace=True)
    events_list = list(events_df['event'])
    start_already_gripping = condition['start_already_gripping']

    # to be consistent with the capability level PI, if the robot should grip the handle by itself then we only consider the checkpoints if the robot was able to grip the handle.
    if not start_already_gripping and 'handle_is_touched' not in events_list:
        # the robot failed to grip the handle. checkpoint time is considered timeout even if for some reason the checkpoint was reached
        target_event_time = 'TIMEOUT'
    else:
        start_moving_event_df = events_df.loc[events_df['event'] == 'cart_starts_moving']
        target_event_df = events_df.loc[events_df['event'] == 'checkpoint_1']
        if len(target_event_df) > 0 and len(start_moving_event_df) > 0:
            start_moving_event = start_moving_event_df.iloc[-1]
            target_event = target_event_df.iloc[-1]
            target_event_time = float(target_event['time']) - float(start_moving_event['time'])
        else:
            target_event_time = 'TIMEOUT'

    # Write result yaml file
    filepath = path.join(output_dir, 'time_to_checkpoint_1.yaml')
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': target_event_time,
        }, result_file, default_flow_style=False)


def run_pi(event_path, condition_path, output_folder_path):
    with open(condition_path, 'r') as condition_file:
        condition_dict = yaml.safe_load(condition_file)

    performance_indicator({'event': event_path}, condition_dict, output_folder_path, datetime.now())
    return 0


if __name__ == '__main__':
    arg_len = 4
    script_name = 'time_to_checkpoint_1'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py event.csv condition.yaml output_dir".format(script_name=script_name)
        exit(-1)

    event_path, condition_path, output_folder_path = argv[1:]

    run_pi(event_path, condition_path, output_folder_path)