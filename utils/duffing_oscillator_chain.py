# -*- coding: utf-8 -*-
""" Time series data from a chain of Duffing oscillators

Part of the accompanying code for the paper "Exploring localization in nonlinear oscillator systems through 
network-based predictions" by C. Geier and N. Hoffmann published in Chaos 35 
(5) 2025 doi: 10.1063/5.0265366 . Available at https://arxiv.org/abs/2407.05497

Chain of coupled Duffing oscillators.
- each oscillator is driven
- whether the oscillators are coupled in a cycle or a chain is determined through the setup of the stiffness matrix K
- forcing amplitude can be defined individually for each mass, but not the forcing frequency.

Use "solve_duffing_chain" to integrate.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""

import numpy as np


def duffing_oscillator_chain(t, x, n, M, K, D, A_ext, omega_ext, k_nl):
    """
    chain of n cyclically coupled nonlinear duffing-type oscillators with mass matrix M, stiffness matrix K and damping
    matrix D,
    and external forcing F_ext = A_ext*cos(omega_ext*t) which acts equally on all oscillators.
    SOE:
    \dot{x} = [zeros(n), eye(n); -K/M, -D/M]*x  + [zeros(n); F_ext/M] + [zeros(n); -F_nl/M]
    :param t: time
    :param x: displacement/velocity vector in phase space (n x 1)
    :param n: number of oscillators
    :param M: mass matrix (n x n)
    :param K: stiffness matrix (n x n)
    :param D: damping matrix (n x n)
    :param A_ext: vector defining forcing amplitude for each oscillator (n x 1)
    :param omega_ext: external forcing frequency (1)
    :param k_nl: nonlinear coupling spring stiffness
    :return: xp (n x 1)
    """

    M_K = np.linalg.lstsq(M, K, rcond=None)[0]
    M_D = np.linalg.lstsq(M, D, rcond=None)[0]
    M_inv = np.linalg.inv(M)

    # simple forcing:
    # -> homogeneous, where A_ext1 = np.ones(n)
    # -> excite a specific mode i when A_ext1 = PHI[:,i]
    M_Fex = M_inv.dot(A_ext)*np.cos(omega_ext*t)

    # add nonlinear restoring force from nonlinear spring between oscillator and ground
    F_nl = np.zeros(n)
    for i in range(n):
        F_nl[i] = k_nl*x[i]**3
    M_Fnl = M_inv.dot(F_nl)

    xp = np.concatenate((
        np.concatenate((np.zeros((n, n)), np.eye(n)), axis=1),
        np.concatenate((-M_K, -M_D), axis=1)
        ), axis=0).dot(x) \
        + np.concatenate((np.zeros(n),M_Fex), axis=0) \
        + np.concatenate((np.zeros(n),-M_Fnl), axis=0)

    return xp


def solve_duffing_chain(t, x0, n, M, K, D, A_ext, omega_ext, knl):
    # sol = solve_duffing_chain(t,x0,n,M,K,D,A_ext,omega_ext,knl)

    """
    Integrate system of n coupled Duffing oscillators.

    :param t: time
    :param x0: initial displacement/velocity vector in phase space (n x 1)
    :param n: number of oscillators
    :param M: mass matrix (n x n)
    :param K: stiffness matrix (n x n)
    :param D: damping matrix (n x n)
    :param A_ext: vector defining forcing amplitude for each oscillator (n x 1)
    :param omega_ext: external forcing frequency (1)
    :param k_nl: nonlinear coupling spring stiffness
    :return: sol (n_timesteps x n)
    """

    from scipy.integrate import ode

    # get start and end time from t
    tstart = t[0]
    tend = t[-1]
    N = np.shape(t)[0]

    # define solver settings
    solver = ode(duffing_oscillator_chain)
    solver.set_integrator('dopri5')         # use an explicit runge-kutta order (4)5 method, equivalent to ode45 in matlab
    solver.set_f_params(n, M, K, D, A_ext, omega_ext, knl)  # give the values
    # of the function parameters to the solver
    solver.set_initial_value(x0, tstart)    # set an initial value
    sol = np.empty((N, 2*n))                # initialize solution array (N_timesteps x 2*n_oscillators)
    sol[0] = np.squeeze(x0)                 # set the first entry in the sol array to the initial conditions

    # solve system
    k = 1
    while solver.successful() and solver.t < tend:
        solver.integrate(t[k])
        sol[k] = solver.y
        k += 1

    return sol
