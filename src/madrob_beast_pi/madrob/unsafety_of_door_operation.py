#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd
import numpy as np
from scipy.signal import iirfilter, lfilter


def performance_indicator(preprocessed_filenames_dict, _, output_dir, start_time):

    critical_frequency = 2.0  # Hz, must be smaller than the Nyquist frequency
    filter_order = 5
    filter_type = 'butter'

    # Load csv as pandas DataFrame
    df = pd.read_csv(preprocessed_filenames_dict['jointState'], skipinitialspace=True)

    acceleration = df['acceleration'][df['acceleration'].notnull()]

    delta = (df['time'][df.index[-1]] - df['time'][0]) / (len(df['time']) - 1)

    # Low-pass filter
    nyquist_frequency = 1./delta/2
    normalised_critical_frequency = critical_frequency / nyquist_frequency

    if critical_frequency > nyquist_frequency:
        print "[Performance Indicator unsafety_of_door_operation] Warning: critical_frequency > nyquist_frequency"
        normalised_critical_frequency = 1.0

    b, a = iirfilter(filter_order, normalised_critical_frequency, btype='lowpass', ftype=filter_type)

    # Low-pass filtered acceleration
    acceleration_lpf = lfilter(b, a, acceleration)

    # Compute result (note: the values in a are broadcasted, see google.com/search?q=numpy+broadcasting)
    unsafety_of_door_operation = float(np.max(np.abs(acceleration_lpf)))

    # Write result yaml file
    filepath = path.join(output_dir, 'unsafety_of_door_operation.yaml')
    with open(filepath, 'w+') as result_file:
        yaml.dump({
            'type': 'scalar',
            'value': unsafety_of_door_operation,
        }, result_file, default_flow_style=False)


def run_pi(joint_state_path, output_folder_path):
    performance_indicator({'jointState': joint_state_path}, None, output_folder_path, datetime.now())
    return 0


if __name__ == '__main__':
    arg_len = 3
    script_name = 'unsafety_of_door_operation'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py jointState.csv output_dir".format(script_name=script_name)
        exit(-1)

    joint_state_path, output_folder_path = argv[1:]
    run_pi(joint_state_path, output_folder_path)
