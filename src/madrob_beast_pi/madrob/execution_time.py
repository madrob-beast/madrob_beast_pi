#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd


def performance_indicator(preprocessed_filenames_dict, testbed_conf, output_dir, start_time):

    execution_time = 'TIMEOUT'

    events_df = pd.read_csv(preprocessed_filenames_dict['events'], skipinitialspace=True)

    if testbed_conf['Robot approach side'] == 'CW':
        destination_side = 'ccw'
    else:
        destination_side = 'cw'

    # Check if there's a 'door_close' event
    door_closes_events = events_df.loc[events_df['event'] == 'door_closes']
    if len(door_closes_events) > 0:
        last_door_close = door_closes_events.iloc[-1]

        # Check if the robot has moved to the destination side
        robot_moves_to_dest_events = events_df.loc[events_df['event'] == 'humanoid_moves_to_{}_side'.format(destination_side)]
        if len(robot_moves_to_dest_events) > 0:
            robot_moves_to_dest = robot_moves_to_dest_events.iloc[0]

            # Check if the last door closing event occurs after the robot moves to destination
            if last_door_close['time'] > robot_moves_to_dest['time']:
                execution_time = float(last_door_close['time']) - float(events_df.loc[events_df['event'] == 'benchmark_start']['time'])

    # Write result yaml file
    filepath = path.join(output_dir, 'execution_time_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': execution_time,
        }, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 4
    script_name = 'execution_time'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py events.csv testbed_config.yaml output_dir".format(script_name=script_name)
        exit(-1)

    events_path, testbed_conf_path, output_folder_path = argv[1:]

    with open(testbed_conf_path, 'r') as testbed_conf_file:
        testbed_conf_dict = yaml.safe_load(testbed_conf_file)

    performance_indicator({'events': events_path}, testbed_conf_dict, output_folder_path, datetime.now())
