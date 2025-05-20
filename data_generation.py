# -*- coding: utf-8 -*-
""" main file for data generation.

Part of the accompanying code for the paper "Exploring localization in nonlinear oscillator systems through 
network-based predictions" by C. Geier and N. Hoffmann published in Chaos 35 
(5) 2025 doi: 10.1063/5.0265366 . Available at https://arxiv.org/abs/2407.05497

Generate time series data by integrating a Duffing oscillator system with a
given set of parameters. The code contains the following steps:
1. generate random initial conditions in within a specified range
2. compute time series data for Duffing oscillator chain with n oscillators
for a set of parameter variations

To reproduce the results in the paper, run the code with settings:
    # define number of oscillators
    n = 10

    # number of initial conditions
    number_of_ic = 100

    # number of parameter variations
    n_vars = 101

    # simulation end time
    tend = 25

    which generates three sets of data used in the paper:
    1. homogeneous_ic1: homogeneous system, x0 in [0, 0.1] (-> Figure 2)
    2. homogeneous_ic2: homogeneous system, x0 in [0, 0.01] (-> Figure 3)
    3. heterogeneous_ic1: heterogeneous system, x0 in [0, 0.1] (-> Figure 4)


Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""

import numpy as np
import os
from utils.utils import load_json, get_settings
from utils.generate_random_ic import generate_random_ic
from utils.oscillator_matrices import stiffness_matrix, mass_matrix, \
    damping_matrix
from utils.duffing_oscillator_chain import solve_duffing_chain
from plots.plot_sectors import plot_sectors_standalone


def compute_duffing_over_ic(dataset_name, directory,
                            t, dt, tend, x0s,
                            n, M, K, D, A_ext, Omega, knl):
    """
    Generate time series of Duffing oscillator cartesian (displacement) coordinates for
    a set of initial conditions.

    Data is stored in the directory "directory"

    :param dataset_name: name of data set
    :param directory: directory for data storage
    :param t: time vector
    :param dt: time step size
    :param tend: simulation end time
    :param x0s: set of initial conditions
    :param n: number of oscillators
    :param M: mass matrix
    :param K: stiffness matrix
    :param D: damping matrix
    :param A_ext: external forcing amplitudes, vector
    :param Omega: external forcing frequency
    :param knl: nonlinear stiffness
    :return:
    """

    # loop over ic starts here
    n_x0s = np.shape(x0s)[1]

    for n_x0 in range(n_x0s):
        # data_name
        data_name = f'{dataset_name}_ic{n_x0}'

        # get initial condition
        x0 = x0s[:, n_x0]

        # compute solution in cartesian coordinates
        sol = solve_duffing_chain(t, x0, n, M, K, D, A_ext, Omega, knl)

        # save data
        np.save(os.path.join(directory, f'{data_name}_c'), sol)

        # plot and save corresponding displacements
        plot_sectors_standalone(sol,
                                10,
                                add_ticks=True,
                                x_ticks=np.linspace(0, int(tend / dt), 6),
                                x_tick_labels=np.linspace(0, tend, 6),
                                y_ticks=np.arange(1, 10, 2),
                                y_tick_labels=np.arange(2, 11, 2),
                                vmin=-1.5,
                                vmax=1.5,
                                savefig=True,
                                figure_path=os.path.join(directory,
                                                         f'{data_name}.jpg'),
                                closefig=True
                                )


def data_generation(dataset_name, higher_directory, n, n_vars, tend, x0s, **kwargs):
    """
    Dataset generation.

    :param dataset_name:
    :param higher_directory:
    :param n: number of oscillators
    :param n_vars: number of parameter variables
    :param tend: simulation end time
    :param x0s: set of initial conditions
    :return:
    """

    # define random variation in parameters
    random_var_m = kwargs.get('random_var_m', False)
    random_var_kl = kwargs.get('random_var_kl', False)
    random_var_kc = kwargs.get('random_var_kc', False)

    """ parameter variations etc """

    # 0. generate a directory to store the data
    result_directory = os.path.join(higher_directory, dataset_name)
    os.mkdir(result_directory)

    # define parameter variation in percent
    m_vars = np.linspace(1, 0.8, num=n_vars)
    np.save(os.path.join(result_directory, 'm-_vars.npy'), m_vars)

    """ setup model """

    # 1. load parameter values
    # define set of parameters to use
    parameter_name = 'my_standard'

    # get standard parameter settings
    d = load_json('utils/duffing_parameters.json')

    # unpack system values
    m, alpha, beta, kl, knl, kc, F, Omega = get_settings(parameter_name, d)

    # force all masses with full amplitude F
    A_ext = np.ones(n) * F

    # define simulation settings
    dt = 0.05
    tstart = 0

    # define integration time
    N = int((tend - tstart) / dt)  # get number of time steps
    t = np.linspace(0, tend, N)  # obtain integration time
    np.save(os.path.join(result_directory, 't.npy'), t)

    """ obtain data """

    # loop over variations of m
    for m_var in m_vars:

        # create a directory to store the data order according to value of m
        directory_m = os.path.join(result_directory, f'{m_var}')
        os.mkdir(directory_m)

        # create name for data with m_var
        dataset_m_name = f'{dataset_name}_m{m_var}'

        # setup model matrices

        K = stiffness_matrix(n, kc, kl,
                             random_var=random_var_kl,
                             random_var_kc=random_var_kc)

        M = mass_matrix(n, m,
                        random_var=random_var_m)

        # introduce the imperfection to the model
        M[3, 3] = m*m_var

        D = damping_matrix(alpha, beta, K, M)

        # compute and store time series data in modal and cartesian coordinates in loop over the ic
        compute_duffing_over_ic(dataset_m_name, directory_m,
                                t, dt, tend, x0s,
                                n, M, K, D, A_ext, Omega, knl)


if __name__ == '__main__':

    """ define preliminaries
    
    - path for data storage
    - model settings
    - number of parameter variations
    
    """

    # define location for storing data
    directory = 'data'

    # define number of oscillators
    n = 10

    # number of initial conditions
    number_of_ic = 3

    # number of parameter variations
    n_vars = 3

    # simulation end time
    tend = 25

    """ generate random initial conditions """

    # for ic1, chose xmax=0.1:
    x0s_1 = generate_random_ic(n, number_of_ic, xmax=0.1,
                               path=os.path.join(directory, 'x0s_1.npy'),
                               create_figure=True)

    # for ic2, chose xmax=0.01
    x0s_2 = generate_random_ic(n, number_of_ic, xmax=0.01,
                               path=os.path.join(directory, 'x0s_2.npy'),
                               create_figure=True)

    """ data generation
    
    generates three sets of data used in the paper
    1. homogeneous_ic1: homogeneous system, x0 in [0, 0.1] (-> Figure 2)
    2. homogeneous_ic2: homogeneous system, x0 in [0, 0.01] (-> Figure 3)
    3. heterogeneous_ic1: heterogeneous system, x0 in [0, 0.1] (-> Figure 4)
        
    """

    # for homogeneous data:
    dataset_name_1 = 'homogeneous_ic1'
    data_generation(dataset_name_1, directory, n, n_vars, tend, x0s_1)

    dataset_name_2 = 'homogeneous_ic2'
    data_generation(dataset_name_2, directory, n, n_vars, tend, x0s_2)

    # for heterogeneous data:
    # 1% random variation on all m, k, knl
    dataset_name_3 = 'heterogeneous_ic1'
    data_generation(dataset_name_3, directory, n, n_vars, tend, x0s_1,
                    random_var_kc=True,
                    random_var_m=True,
                    random_var_kl=True)



