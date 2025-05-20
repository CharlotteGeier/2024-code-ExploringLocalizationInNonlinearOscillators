# -*- coding: utf-8 -*-
""" main file analysis of node in-degrees within functional network

Part of the accompanying code for the paper "Exploring localization in nonlinear oscillator systems through 
network-based predictions" by C. Geier and N. Hoffmann published in Chaos 35 
(5) 2025 doi: 10.1063/5.0265366 . Available at https://arxiv.org/abs/2407.05497

Analysis of functional networks:
- Compute node in- and out-degree for each node.
- Get mean values and standard deviation for parameter variation.

To reproduce results in the paper, fill in the appropriate paths below.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""


import networkx as nx
from matplotlib import pyplot as plt
import os
import numpy as np

def get_ordered_out_degree(G):
    """
    Get in-degrees from a graph G listed by node name.
    :param G:
    :return:
    """
    # get in degrees in list form
    out_degree_list = [[int(node), val] for (node, val) in G.out_degree()]

    # sort list by node name
    sorted_list = sorted(out_degree_list)

    # get in-degrees only
    sorted_out_degrees = [val for (node, val) in sorted_list]

    return sorted_out_degrees


def get_ordered_in_degree(G):
    """
    Get in-degrees from a graph G listed by node name.
    :param G:
    :return:
    """
    # get in degrees in list form
    in_degree_list = [[int(node), val] for (node, val) in G.in_degree()]

    # sort list by node name
    sorted_list = sorted(in_degree_list)

    # get in-degrees only
    sorted_in_degrees = [val for (node, val) in sorted_list]

    return sorted_in_degrees


def get_degree_means_and_stds(path_study, m_vars, x0s, n):
    """
    Compute mean in- and out-degree and respective standard deviation of nodes over a set of networks.
    Specifically:
    - folder structure: path_study/<parameter variations>/<various initial conditions>/networks
    - for each parameter variation, the mean and std in- and out degree over the set of IC is computed
    :param path_study: path to study (e.g. 202312_isrn_shm/isrn_shm_10_0)
    :param m_vars: list of parameter variations, have to match <parameter variations> directories
    :param n: number of oscillators in the system (=number of modal or cartesian coordinates)
    :return: means_cart, stds_cart, means_cart_in, stds_cart_in
           where:
           - means: means and stds are standard deviations
           - _in: in-degrees, else: out-degrees
           - _cart: cartesian coords. network only
           - shape: cart, [n, n_ic]

    """


    # get number of variations of m, # of different ic
    n_m_vars = np.shape(m_vars)[0]
    n_ics = np.shape(ics)[1]

    # setup an array n_ic x n x n_mvars
    out_degree_cart_array = np.zeros((n_ics, n, n_m_vars))
    in_degree_cart_array = np.zeros((n_ics, n, n_m_vars))

    # set counter over variations of parameter m
    i_m_var = 0

    # compute values for one variation of m
    for m_var in m_vars:

        path_m_var = os.path.join(path_study, f'{m_var}')

        # set counter over initial conditions
        i_ic = 0

        # loop over all ic for one variation of m
        for ic in os.listdir(path_m_var):
            path_ic = os.path.join(path_m_var, ic)
            print(f'Loading graph {path_ic}.')

            # load cartesian net
            G_cart = nx.read_edgelist(os.path.join(path_ic, 'G_cartesian'),
                                      create_using=nx.DiGraph)

            # compute out-degrees
            dout_cart = get_ordered_out_degree(G_cart)

            din_cart = get_ordered_in_degree(G_cart)

            # add computed out degrees to array
            out_degree_cart_array[i_ic, :, i_m_var] = np.array(dout_cart)

            in_degree_cart_array[i_ic, :, i_m_var] = np.array(din_cart)

            i_ic = i_ic + 1

        i_m_var = i_m_var + 1

    # compute the mean and std dev along the first (ic) axis: n x n_mvars array
    means_cart = np.mean(out_degree_cart_array, axis=0)
    stds_cart = np.std(out_degree_cart_array, axis=0)

    means_cart_in = np.mean(in_degree_cart_array, axis=0)
    stds_cart_in = np.std(in_degree_cart_array, axis=0)

    return means_cart, stds_cart,means_cart_in, stds_cart_in


if __name__ == '__main__':


    # define location of study
    path_study = 'results/funcnet_homogeneous_ic1_10s_no_noise'
    path_data = 'data/homogeneous_ic1'
    path_ic = 'data/x0s_1.npy'

    # store the results in a proper location
    result_name = 'degrees_funcnet_homogeneous_ic1_10s_no_noise'
    result_path = f'results/{result_name}'


    # load variations of parameter and initial conditions
    m_vars = np.load(os.path.join(path_data, 'm-_vars.npy'))
    ics = np.load(path_ic)
    xlabel = 'm 4'

    # define number of components
    n = 10


    """ computations below """

    # compute means and stds

    means_cart, stds_cart, means_cart_in, stds_cart_in, \
        = get_degree_means_and_stds(path_study, m_vars, ics, n)



    # change name if directory already exists to avoid overwriting
    if os.path.isdir(result_path):
        result_path = f'{result_path}_1'
    os.mkdir(result_path)

    np.save(os.path.join(result_path, f'{result_name}_means_cart.npy'), means_cart)
    np.save(os.path.join(result_path, f'{result_name}_stds_cart.npy'), stds_cart)

    np.save(os.path.join(result_path, f'{result_name}_means_cart_in.npy'), means_cart_in)
    np.save(os.path.join(result_path, f'{result_name}_stds_cart_in.npy'), stds_cart_in)

    """ plots """

    from plots.plot_in_degree import plot_in_degrees

    fig, ax = plt.subplots(1, 1, figsize=(3, 3))
    plot_in_degrees(means_cart_in, stds_cart_in, m_vars, ax)

    # figure export setup (size, resolution) (84mm or 174 mm width)
    width_, height_, resolution = 8.4, 5.5, 300
    fig.set_size_inches(width_ * 0.3937,
                        height_ * 0.3937)  # this is only inches. convert cm to inch by * 0.3937007874

    # figure export as impage and png image of certain size and resolution
    figure_name = result_name
    plt.savefig(os.path.join(result_path, figure_name),
                dpi=resolution,
                bbox_inches="tight")  # bbox_inches takes care of keeping everything inside the frame that is being exported

    plt.show()



