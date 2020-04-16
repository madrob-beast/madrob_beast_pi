#!/usr/bin/env python
# coding=utf-8

import yaml
from os import path
from sys import argv, exit
from datetime import datetime

import pandas as pd
import numpy as np
from scipy.signal import iirfilter, lfilter
import matplotlib.pyplot as plt


def performance_indicator(preprocessed_filenames_dict, _, output_dir, start_time):

    critical_frequency = 2.0  # Hz, must be smaller than the Nyquist frequency
    filter_order = 5
    filter_type = 'butter'

    # Load csv as pandas DataFrame
    df = pd.read_csv(preprocessed_filenames_dict['door_angular_acceleration'], skipinitialspace=True)

    # Handle force timeseries
    acceleration = df['door_angular_acceleration']
    delta = (df['timestamp'][df.index[-1]] - df['timestamp'][0]) / (len(df['timestamp']) - 1)

    # Low-pass filter
    nyquist_frequency = 1./delta/2
    normalised_critical_frequency = critical_frequency / nyquist_frequency

    if critical_frequency > nyquist_frequency:
        print "[Performance Indicator unsafety_of_door_operation] Warning: critical_frequency > nyquist_frequency"
        normalised_critical_frequency = 1.0

    b, a = iirfilter(filter_order, normalised_critical_frequency, btype='lowpass', ftype=filter_type)

    # Low-pass filtered acceleration
    a = lfilter(b, a, acceleration)

    # Compute result (note: the values in a are broadcasted, see google.com/search?q=numpy+broadcasting)
    unsafety_of_door_operation = float(np.max(np.abs(a)))
    print 'unsafety_of_door_operation', unsafety_of_door_operation, 'rad/s²'

    # Write result yaml file
    filepath = path.join(output_dir, 'unsafety_of_door_operation_%s.yaml' % (start_time.strftime('%Y%m%d_%H%M%S')))
    with open(filepath, 'w+') as result_file:
        yaml.dump({'unsafety_of_door_operation': unsafety_of_door_operation}, result_file, default_flow_style=False)


if __name__ == '__main__':
    arg_len = 3
    script_name = 'unsafety_of_door_operation'
    if len(argv) != arg_len:
        print "[Performance Indicator {script_name}] Error: arguments must be {script_name}.py door_angular_acceleration.csv output_dir".format(script_name=script_name)
        exit(-1)

    door_angular_acceleration_path, output_folder_path = argv[1:]
    performance_indicator({'door_angular_acceleration': door_angular_acceleration_path}, None, output_folder_path, datetime.now())
