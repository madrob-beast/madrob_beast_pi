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
    df = pd.read_csv(preprocessed_filenames_dict['distance'], skipinitialspace=True)

    # Handle force timeseries
    df['time'] = df['time'] - df['time'].iloc[0]
    r = df['distance']

    # Compute result (note: the values in r are broadcasted, see google.com/search?q=numpy+broadcasting)
    safety_of_navigation = float(np.min(r))

    # Write result yaml file
    filepath = path.join(output_dir, 'safety_of_navigation.yaml')
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': safety_of_navigation,
        }, result_file, default_flow_style=False)


def run_pi(distance_path, output_folder_path):
    performance_indicator({'distance': distance_path}, None, output_folder_path, datetime.now())
    return 0


if __name__ == '__main__':
    arg_len = 3
    script_name = 'safety_of_navigation'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py distance.csv output_dir".format(script_name=script_name)
        exit(-1)

    distance_path, output_folder_path = argv[1:]
    run_pi(distance_path, output_folder_path)
