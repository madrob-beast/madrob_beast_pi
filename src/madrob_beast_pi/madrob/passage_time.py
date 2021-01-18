#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, testbed_conf, output_dir, start_time):

    passage_time = 'TIMEOUT'

    events_df = pd.read_csv(preprocessed_filenames_dict['events'], skipinitialspace=True)

    if testbed_conf['robot_approach_side'] == 'CW':
        destination_side = 'ccw'
    else:
        destination_side = 'cw'

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


def run_pi(events_path, testbed_conf_path, output_folder_path):
    with open(testbed_conf_path, 'r') as testbed_conf_file:
        testbed_conf_dict = yaml.safe_load(testbed_conf_file)

    performance_indicator({'events': events_path}, testbed_conf_dict, output_folder_path, datetime.now())
    return 0


if __name__ == '__main__':
    arg_len = 4
    script_name = 'passage_time'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py events.csv testbed_config.yaml output_dir".format(script_name=script_name)
        exit(-1)

    events_path, testbed_conf_path, output_folder_path = argv[1:]

    run_pi(events_path, testbed_conf_path, output_folder_path)