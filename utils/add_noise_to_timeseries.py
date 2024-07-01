# -*- coding: utf-8 -*-
""" Add Gaussian white noise to a time series.

Part of the accompanying code for the paper "Exploring localization in
nonlinear oscillator systems through network-based predictions" by Charlotte
Geier and Norbert Hoffmann submitted to the Journal of Sound and Vibration in July 2024.

Input time series. Gaussian white noise is defined by its mean and standard
deviation.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""

import numpy as np

def add_noise_to_timeseries(time_series, **kwargs):
    """
    Add Gaussian white noise to time series [n_time_steps, n_variables].
    :param time_series:
    :param kwargs:
    :return:
    """

    mean = kwargs.get('mean', 0)
    std_mode = kwargs.get('std_mode')
    std = kwargs.get('std', 0.01)

    # get number of variables and number of time steps
    [num_samples, num_vars] = np.shape(time_series)

    # initialize noisy time series as the original time series
    noisy_time_series = time_series

    # loop over all variables in the time series
    for i in range(num_vars):

        # if required, compute the standard deviation of the noise from the time series amplitude
        if std_mode == 'from_ts':
            std_ts = np.std(noisy_time_series[:,i])
            std = std_ts*0.05

        # generate white noise
        noise = np.random.normal(mean, std, size=num_samples)

        # add noise to each time series
        noisy_time_series[:, i] = noisy_time_series[:, i] + noise

    return noisy_time_series

