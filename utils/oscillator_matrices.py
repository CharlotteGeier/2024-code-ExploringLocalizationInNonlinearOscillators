# -*- coding: utf-8 -*-
""" Setup Duffing Oscillator matrices.

Part of the accompanying code for the paper "Exploring localization in nonlinear oscillator systems through 
network-based predictions" by C. Geier and N. Hoffmann published in Chaos 35 
(5) 2025 doi: 10.1063/5.0265366 . Available at https://arxiv.org/abs/2407.05497

Stiffness matrix K, mass matrix M and damping matrix (Rayleigh) D.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""


import numpy as np


def get_random_diag(n, percent, variable, **kwargs):
    """ Generate an (n,) array of random numbers in [-percent*variable, percent*variable] """

    seed = kwargs.get('seed', 111)

    # set random seed
    np.random.seed(seed)

    # create a set of n random numbers in [-1,1]
    diag = 2 * np.random.rand(n) - 1

    # adjust the range to the desired percentage and linear stiffness value
    bound = percent * variable
    diag_bound = diag * bound

    return diag_bound


def stiffness_matrix(n, kc, kl, **kwargs):
    """
    compute the stiffness matrix for a cyclic oscillator chain with linear stiffness
    setup:
        K = np.diag(2*kc*np.ones(n)) \       # coupling, 2*kc along main diagonal
            + np.diag(-kc*np.ones(n-1),1) \  # coupling with oscilallaotr i+1, along subdiagonal
            + np.diag(-kc*np.ones(n-1),-1) \ # coupling with oscilallaotr i-1, along subdiagonal
            + np.diag(-kc*np.ones(1),n-1) \  # cyclic connector of first with last element
            + np.diag(-kc*np.ones(1),-n+1) \ # cyclic connector of last with first element
            + np.diag(kl*np.ones(n))         # linear spring, values along main diagonal
    :param n: number of oscillators
    :param kc: coupling stiffness
    :param kl: linear spring connected to ground
    :param kwargs: mode: 'cyclic' or 'linear'. whether or not the oscillator chain is closed or open.
    :param kwargs: random_var: set True to incorporate a 5% random variation of the linear spring stiffness. only works for kl = 1
    :return: the stiffness matrix K
    """

    random_var = kwargs.get('random_var')  # random variation of linear spring stiffness
    random_var_kc = kwargs.get('random_var_kc')  # random variation of coupling spring stiffness
    percent = kwargs.get('percent', 0.01)

    K = np.diag(2*kc*np.ones(n)) \
        + np.diag(-kc*np.ones(n-1), 1) \
        + np.diag(-kc*np.ones(n-1), -1) \
        + np.diag(-kc*np.ones(1), n-1) \
        + np.diag(-kc*np.ones(1), -n+1) \
        + np.diag(kl*np.ones(n))

    if random_var:
        # get array of random values in [-percent*kl, percent*kl] to add to K
        diag_bound = get_random_diag(n, percent, kl, seed=111)

        # make a diagonal matrix
        K_var_kl = np.diag(diag_bound)

        # add diagonal matrix K_var to original stiffness matrix K to create randomly varied K
        K = K + K_var_kl

    if random_var_kc:
        # get random small entries to add to K
        diag_bound_1 = get_random_diag(n - 1, percent, kc, seed=112)
        diag_bound_2 = get_random_diag(n - 1, percent, kc, seed=113)
        diag_bound_3 = get_random_diag(1, percent, kc, seed=114)
        diag_bound_4 = get_random_diag(1, percent, kc, seed=115)

        # make a diagonal matrix
        K_var_kc = np.diag(diag_bound_1, k=-1) + np.diag(diag_bound_2, k=1) + np.diag(diag_bound_3, k=-(n-1)) + np.diag(
            diag_bound_4, k=(n-1))

        # add diagonal matrix K_var to original stiffness matrix K to create randomly varied K
        K = K + K_var_kc

    return K


def mass_matrix(n, m, **kwargs):
    """
    set up mass matrix for an oscillator chain with n elements.
    :param n: number of oscillators
    :param m: mass of each oscillator
    :return: mass matrix M
    """
    random_var = kwargs.get('random_var')
    percent = kwargs.get('percent', 0.01)

    M = m * np.eye(n, n)

    if random_var:
        # get random variations for diagonal
        diag_bound = get_random_diag(n, percent, m, seed=234)

        # make a diagonal matrix
        M_var = np.diag(diag_bound)

        # add diagonal matrix K_var to original stiffness matrix K to create randomly varied K
        M = M + M_var

    return M


def damping_matrix(alpha, beta, K, M):
    """
    setup damping matrix for Rayleigh damping
    :param alpha: stiffness-proportional damping
    :param beta: mass-proportional damping
    :param K: stiffness matrix
    :param M: mass matrix
    :return: damping matrix D
    """

    D = alpha * M + beta * K

    return D


if __name__ == '__main__':

    n = 5
    kc = 0.1
    kl = 2
    K = stiffness_matrix(n, kc, kl)
    K_rand = stiffness_matrix(n, kc, kl, random_var=True, percent=0.03)