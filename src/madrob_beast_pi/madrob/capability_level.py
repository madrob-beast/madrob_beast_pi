#!/usr/bin/env python2.7
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, condition, output_dir, start_time):

    # Capability level: 0 to 4: approaches door, touches handle, moves to destination side, closes door
    capability_level = 0

    events_df = pd.read_csv(preprocessed_filenames_dict['event'], skipinitialspace=True)

    if condition['robot_approach_side'] == 'CW':
        approach_side = 'cw'
        destination_side = 'ccw'
    else:
        approach_side = 'ccw'
        destination_side = 'cw'

    # Door approach event
    robot_approach_events = events_df.loc[events_df['event'] == 'humanoid_approaches_the_door_on_{}_side'.format(approach_side)]
    if len(robot_approach_events) > 0:
        capability_level += 1

    # Handle is touched event
    handle_is_touched_events = events_df.loc[events_df['event'] == 'handle_is_touched']
    if len(handle_is_touched_events) > 0:
        capability_level += 1

    # Move to destination event
    robot_moves_to_dest_events = events_df.loc[events_df['event'] == 'humanoid_moves_to_{}_side'.format(destination_side)]
    if len(robot_moves_to_dest_events) > 0:
        capability_level += 1

    # Door closes event
    door_closes_events = events_df.loc[events_df['event'] == 'door_closes']
    if len(door_closes_events) > 0:
        capability_level += 1

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


def main ():
    arg_len = 4
    script_name = 'capability_level'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py event.csv condition.yaml output_dir".format(script_name=script_name)
        exit(-1)

    event_path, condition_path, output_folder_path = argv[1:]

    return run_pi(event_path, condition_path, output_folder_path)


if __name__ == '__main__':
    main()
