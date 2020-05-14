#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, testbed_conf, output_dir, start_time):

    door_occupation_time = 'TIMEOUT'

    events_df = pd.read_csv(preprocessed_filenames_dict['events'], skipinitialspace=True)

    if testbed_conf['Robot approach side'] == 'CW':
        approach_side = 'cw'
        destination_side = 'ccw'
    else:
        approach_side = 'ccw'
        destination_side = 'cw'

    # Check if the robot has moved to the destination side
    robot_moves_to_dest_events = events_df.loc[events_df['event'] == 'humanoid_moves_to_{}_side'.format(destination_side)]
    if len(robot_moves_to_dest_events) > 0:
        robot_moves_to_dest = robot_moves_to_dest_events.iloc[0]

        # Check if the robot approach event exists
        robot_approach_events = events_df.loc[events_df['event'] == 'humanoid_approaches_the_door_on_{}_side'.format(approach_side)]
        if len(robot_approach_events) > 0:
            robot_approach = robot_approach_events.iloc[0]

            # Check if 'robot moves to destination' occurs after 'robot approaches the door'
            if robot_moves_to_dest['time'] > robot_approach['time']:
                door_occupation_time = float(robot_moves_to_dest['time']) - float(robot_approach['time'])

    # Write result yaml file
    filepath = path.join(output_dir, 'door_occupation_time_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': door_occupation_time,
        }, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 4
    script_name = 'door_occupation_time'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py events.csv testbed_config.yaml output_dir".format(script_name=script_name)
        exit(-1)

    events_path, testbed_conf_path, output_folder_path = argv[1:]

    with open(testbed_conf_path, 'r') as testbed_conf_file:
        testbed_conf_dict = yaml.safe_load(testbed_conf_file)

    performance_indicator({'events': events_path}, testbed_conf_dict, output_folder_path, datetime.now())
