# -*- coding: utf-8 -*-
""" main file analysis of strongly connected components within functional
networks

Part of the accompanying code for the paper "Exploring localization in nonlinear oscillator systems through 
network-based predictions" by C. Geier and N. Hoffmann published in Chaos 35 
(5) 2025 doi: 10.1063/5.0265366 . Available at https://arxiv.org/abs/2407.05497

Analysis of functional networks:
- Compute strongly connected components and their evolution.
- 1. components for different initial conditions within one parameter
- 2. components for one initial conditions over variation of parameter

To reproduce results in the paper, fill in the appropriate paths below.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""


import numpy as np
import networkx as nx
import os
from plots.plot_components import plot_components_standalone


def compute_clusters_over_ic(path, value):

    input_path = os.path.join(path, value)
    filelist = sorted([f for f in os.listdir(input_path)])

    number_of_graphs = len(filelist)
    number_of_nodes = 10
    node_array = np.zeros([number_of_nodes, number_of_graphs])

    i = 0

    for graph in filelist:
        # read a graph
        G = nx.read_edgelist(os.path.join(input_path, f'{graph}/G_cartesian'),
                             create_using=nx.DiGraph)

        # get strongly connected components for a graph
        scc = list(nx.strongly_connected_components(G))

        # loop over clusters within one graph
        for cluster in scc:

            # transform cluster from set of strings into list of integers
            cluster_list = [int(i) for i in list(cluster)]

            """ compute node array for visualization """

            # get the mean value within a cluster
            number_of_nodes_in_cluster = len(cluster_list)
            mean_value = np.sum(cluster_list) / number_of_nodes_in_cluster

            # loop over each node within a cluster
            shift = 0
            for node in cluster_list:
                # assign each node the lowest value within a cluster
                node_array[node, i] = mean_value + 0.1 * shift

                shift = shift + 1

        i = i + 1

    return node_array


def compute_clusters_over_parameter(input_path, ic, number_of_graphs):
    filelist = sorted([f for f in os.listdir(input_path)])

    number_of_nodes = 10
    node_array = np.zeros([number_of_nodes, number_of_graphs])

    i = 0

    for variable in filelist:
        if not variable.endswith('npy'):
            # read a graph
            G = nx.read_edgelist(os.path.join(input_path,
                                              f'{variable}/homogeneous_ic1_m'
                                                          f'{variable}_'
                                                          f'{ic}/G_cartesian'),
                                 create_using=nx.DiGraph)

            # get strongly connected components for a graph
            scc_unsorted = list(nx.strongly_connected_components(G))
            scc = sorted(scc_unsorted)

            # define cluster locations according to numer of clusters
            j = 0

            # loop over clusters within one graph
            for cluster in scc:

                # transform cluster from set of strings into list of integers
                cluster_list_unsorted = [int(i) for i in list(cluster)]
                cluster_list = sorted(cluster_list_unsorted)

                """ compute node array to visualize evolution of components """

                # loop over each node within a cluster
                shift = 0
                factor = 0.5
                for node in cluster_list:

                    if cluster_list[0] == 4:
                        node_array[node, i] = 1 - 2.5*factor
                    else:
                        # assign each node the lowest value within a cluster
                        node_array[node, i] = 1 - cluster_list[0]*factor - 0.1 * shift

                    shift = shift + 1
                j = j+1

            i = i + 1

    return node_array


if __name__ == '__main__':

    name = 'funcnet_homogeneous_ic1_10s_no_noise'
    input_path = os.path.join('results', name)
    output_path = os.path.join('results', f'clusters_{name}')
    os.mkdir(output_path)

    """ generate cluster data """

    # generate cluster data per variable, e.g. m = '0.8'
    value = '1.0'
    result_name = f'cluster_par_m_{value}_{name}'
    result_path = os.path.join(output_path, f'par_m_{value}')
    os.mkdir(result_path)
    node_array = compute_clusters_over_ic(input_path, value)
    # save array for later use
    np.save(os.path.join(result_path,f'{result_name}.npy'), node_array)


    # # generate cluster data per initial condition, e.g. ic = 'ic21'
    ic = 'ic1'
    result_name = f'cluster_ic_{ic}_{name}'
    result_path = os.path.join(output_path, f'ic_{ic}')
    os.mkdir(result_path)
    node_array = compute_clusters_over_parameter(input_path, ic, 100)
    # save array for later use
    np.save(os.path.join(result_path,f'{result_name}.npy'), node_array)

    """ generate plot """

    figure_name = f'{result_name}.png'
    plot_components_standalone(node_array, os.path.join(result_path,
                                                       figure_name))