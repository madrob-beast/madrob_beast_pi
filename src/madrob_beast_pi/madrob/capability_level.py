#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, testbed_conf, output_dir, start_time):

    # Capability level: 0 to 4: approaches door, touches handle, moves to destination side, closes door
    capability_level = 0

    events_df = pd.read_csv(preprocessed_filenames_dict['events'], skipinitialspace=True)

    if testbed_conf['Robot approach side'] == 'CW':
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
    filepath = path.join(output_dir, 'capability_level_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': capability_level,
        }, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 4
    script_name = 'capability_level'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py events.csv testbed_config.yaml output_dir".format(script_name=script_name)
        exit(-1)

    events_path, testbed_conf_path, output_folder_path = argv[1:]

    with open(testbed_conf_path, 'r') as testbed_conf_file:
        testbed_conf_dict = yaml.safe_load(testbed_conf_file)

    performance_indicator({'events': events_path}, testbed_conf_dict, output_folder_path, datetime.now())
