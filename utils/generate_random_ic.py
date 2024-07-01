# -*- coding: utf-8 -*-
""" Generate random initial conditions

Part of the accompanying code for the paper "Exploring localization in
nonlinear oscillator systems through network-based predictions" by Charlotte
Geier and Norbert Hoffmann submitted to the Journal of Sound and Vibration in July 2024.

Input number of dimensions n, number of variations M, and max value.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""


import numpy as np
from matplotlib import pyplot as plt

def generate_random_ic(n, M, xmax=0.1, **kwargs):
    """
    Generate a set of M initial conditions in (2*n)
    :param n: number of oscillators
    :param M: number a variations
    :param xmax: maximum random number, value to scale array to
    :param kwargs: path where to store result array, incl. name of array
    :return:
    """

    path = kwargs.get('path')
    create_figure = kwargs.get('create_figure')

    # fix random seed for reproducibility
    np.random.seed(2809)

    random_array = np.random.rand(2*n, M)

    # scale array from [0,1] to [0,xmax]
    x0s = random_array*xmax

    # store array
    if path:
        np.save(path, x0s)

    # create a figure if necessary
    if create_figure:
        fig, ax = plt.subplots(nrows=n, figsize=(3, 24))
        for i in range(n):
            ax[i].plot(x0s[i, :], x0s[i + n, :], '.')
            ax[i].set_xlabel(f'x0_{i}')
            ax[i].set_ylabel(f'v0_{i}')
            ax[i].set_aspect('equal')
            ax[i].set_xlim([0, xmax])
            ax[i].set_ylim([0, xmax])
        plt.tight_layout()
        if path:
            plt.savefig(f'{path[:-4]}.jpg')
        plt.show()

    return x0s




if __name__ == '__main__':

    # fix numbero f oscillators
    n = 10

    # define number of variations
    M = 5

    # fix upper limit
    xmax = 0.1

    # generate random initial conditions
    x0s = generate_random_ic(n, M, xmax, path='test.npy', create_figure=True)




