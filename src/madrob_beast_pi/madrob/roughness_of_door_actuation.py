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
    df = pd.read_csv(preprocessed_filenames_dict['wrench'], skipinitialspace=True)

    # Handle force timeseries
    f = df['force_x']

    # Compute result (note: the values in f are broadcasted, see google.com/search?q=numpy+broadcasting)
    roughness_of_door_actuation = float(np.max(np.abs(f)))

    # Write result yaml file
    filepath = path.join(output_dir, 'roughness_of_door_actuation_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': roughness_of_door_actuation,
        }, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 3
    script_name = 'roughness_of_door_actuation'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py wrench.csv output_dir".format(script_name=script_name)
        exit(-1)

    wrench_path, output_folder_path = argv[1:]
    performance_indicator({'wrench': wrench_path}, None, output_folder_path, datetime.now())
