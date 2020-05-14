#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd
import numpy as np


def performance_indicator(preprocessed_filenames_dict, _, output_dir, start_time):

    # Load csv as pandas DataFrame
    df = pd.read_csv(preprocessed_filenames_dict['jointState'], skipinitialspace=True)

    # Handle force timeseries
    a = df['acceleration']

    # Compute result (note: the values in a are broadcasted, see google.com/search?q=numpy+broadcasting)
    smoothness_of_door_actuation = float(100. / np.sqrt(np.sum(a ** 2)))

    # Write result yaml file
    filepath = path.join(output_dir, 'smoothness_of_door_actuation_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': smoothness_of_door_actuation,
        }, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 3
    script_name = 'smoothness_of_door_actuation'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py jointState.csv output_dir".format(script_name=script_name)
        exit(-1)

    joint_state_path, output_folder_path = argv[1:]
    performance_indicator({'jointState': joint_state_path}, None, output_folder_path, datetime.now())
