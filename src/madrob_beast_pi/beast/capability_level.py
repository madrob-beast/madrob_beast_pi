#!/usr/bin/env python2.7
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, condition, output_dir, start_time):

    events_df = pd.read_csv(preprocessed_filenames_dict['event'], skipinitialspace=True)
    start_already_gripping = condition['start_already_gripping']
    events_list = list(events_df['event'])
    checkpoint_events_list = filter(lambda s: "checkpoint_" in s, events_list)

    if start_already_gripping:
        # if the robot starts already gripping, then the capability level is just the number of reached checkpoints.
        # each checkpoint can only be crossed once and in the correct order, so we can just count the number of checkpoint events.
        capability_level = len(checkpoint_events_list)
    else:
        # if the robot does not start already gripping, then the first capability level is whether the robot touched the handle and then the number of reached checkpoints.
        if "handle_is_touched" in events_list:
            capability_level = 1 + len(checkpoint_events_list)
        else:
            # if the robot did not touch the handle the capability level is zero.
            capability_level = 0

    # Write result yaml file
    filepath = path.join(output_dir, 'capability_level.yaml')
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': capability_level,
        }, result_file, default_flow_style=False)


def run_pi(event_path, condition_path, output_folder_path):

    with open(condition_path, 'r') as condition_file:
        condition_dict = yaml.safe_load(condition_file)

    performance_indicator({'event': event_path}, condition_dict, output_folder_path, datetime.now())
    return 0


def main():
    arg_len = 4
    script_name = 'capability_level'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py event.csv condition.yaml output_dir".format(script_name=script_name)
        exit(-1)

    event_path, condition_path, output_folder_path = argv[1:]

    return run_pi(event_path, condition_path, output_folder_path)


if __name__ == '__main__':
    main()
