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

    events_df = pd.read_csv(preprocessed_filenames_dict['events_sequence'], skipinitialspace=True)

    if testbed_conf['Robot approach side'] == 'CW':
        approach_side = 'cw'
        destination_side = 'ccw'
    else:
        approach_side = 'ccw'
        destination_side = 'cw'

    # Door approach event
    robot_approach_events = events_df.loc[events_df['events_sequence'] == 'humanoid_approaches_the_door_on_{}_side'.format(approach_side)]
    if len(robot_approach_events) > 0:
        capability_level += 1
        robot_approach_timestamp = robot_approach_events.iloc[0]['timestamp']

        # Handle is touched event
        handle_is_touched_events = events_df.loc[events_df['events_sequence'] == 'handle_is_touched']
        if len(handle_is_touched_events) > 0:
            handle_is_touched_timestamp = handle_is_touched_events.iloc[0]['timestamp']
            if handle_is_touched_timestamp > robot_approach_timestamp:
                capability_level += 1

                # Move to destination event
                robot_moves_to_dest_events = events_df.loc[events_df['events_sequence'] == 'humanoid_moves_to_{}_side'.format(destination_side)]
                if len(robot_moves_to_dest_events) > 0:
                    robot_moves_to_dest_timestamp = robot_moves_to_dest_events.iloc[0]['timestamp']
                    if robot_moves_to_dest_timestamp > handle_is_touched_timestamp:
                        capability_level += 1

                        # Door closes event
                        door_closes_events = events_df.loc[events_df['events_sequence'] == 'door_closes']
                        if len(door_closes_events) > 0:
                            last_door_close_timestamp = door_closes_events.iloc[-1]['timestamp']
                            if last_door_close_timestamp > robot_moves_to_dest_timestamp:
                                capability_level += 1

    # Write result yaml file
    filepath = path.join(output_dir, 'capability_level_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({'capability_level': capability_level}, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 4
    script_name = 'capability_level'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py events_sequence.csv testbed_config.yaml output_dir".format(script_name=script_name)
        exit(-1)

    events_sequence_path, testbed_conf_path, output_folder_path = argv[1:]

    with open(testbed_conf_path, 'r') as testbed_conf_file:
        testbed_conf = yaml.load(testbed_conf_file)

    performance_indicator({'events_sequence': events_sequence_path}, testbed_conf, output_folder_path, datetime.now())
