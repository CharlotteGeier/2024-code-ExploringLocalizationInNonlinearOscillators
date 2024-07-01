# -*- coding: utf-8 -*-
""" Plot evolution of strongly connected network components.

Part of the accompanying code for the paper "Exploring localization in
nonlinear oscillator systems through network-based predictions" by Charlotte
Geier and Norbert Hoffmann submitted to the Journal of Sound and Vibration in July 2024.

Input a node array computed via compute_components.py
Use plot_components_standalone for standalone figure.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024

"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl


def plot_components(node_array, ax, **kwargs):

    linewidth = kwargs.get('linewidth', 3)
    plot_legend = kwargs.get('plot_legend', True)
    ylabel = kwargs.get('ylabel', 'SCC')
    xlabel = kwargs.get('xlabel')
    settings = kwargs.get('settings','test')

    number_of_nodes = np.shape(node_array)[0]

    # define colormap for blueish lines
    colors = mpl.cm.Blues(np.linspace(0.5, 1, number_of_nodes))


    for j in range(number_of_nodes):
        if j == 3:
            ax.plot(node_array[j, :], 'tab:red',label=f'$n_{j+1}$', linewidth=linewidth)
        elif j == 9:
            ax.plot(node_array[j, :], label='$n_{10}$', linewidth=linewidth, color=colors[j])
        else:
            ax.plot(node_array[j, :], label=f'$n_{j+1}$', linewidth=linewidth, color=colors[j])

    # plot red line again on top of everything
    ax.plot(node_array[3, :], 'tab:red', linewidth=linewidth)

    if plot_legend:
        ax.legend(ncols=10,
                  columnspacing=0.08,
                  borderpad=0.1,
                  handlelength=0.8,
                  labelspacing=0.08,
                  loc='upper left')

    ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)

    ax.set_xticks([])
    ax.set_xlim([0, np.shape(node_array)[1]-1])

    if settings == 'overview1':
        ax.set_yticks([])
        ax.set_ylim([-0.8, 2])
    elif settings == 'overview2':
        ax.set_yticks([])
        ax.set_ylim([-0.8, 2])
    elif settings == 'robustness':
        ax.set_yticks([])
        ax.set_ylim([-0.8, 2])
        ax.set_xticks(np.linspace(0, 100, 9))
        ax.set_xticklabels(np.round(np.linspace(0.8, 1, 9), decimals=3))



def plot_components_standalone(node_array, figure_name):
    """ generate the plot """

    plt.style.use("default")  # dark_background

    # set LaTeX font
    tex_fonts = {
        # Use LaTeX to write all text
        "text.usetex": True,
        "font.family": "serif",
        # Use 10pt font in plots, to match 10pt font in document
        "axes.titlesize": 10,
        "axes.labelsize": 10,
        "font.size": 10,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8
    }
    plt.rcParams.update(tex_fonts)

    fig, ax = plt.subplots(1, 1)

    plot_components(node_array, ax)

    # figure export setup (size, resolution) (84mm or 174 mm width)
    width_, height_, resolution = 8.4, 3, 300
    fig.set_size_inches(width_ * 0.3937,
                        height_ * 0.3937)  # this is only inches. convert cm to inch by * 0.3937007874

    # figure export as impage and png image of certain size and resolution
    # plt.savefig(figure_name, dpi=resolution,
    #             bbox_inches='tight')  # bbox_inches takes care of keeping everything inside the frame that is being exported

    plt.show()


if __name__ == '__main__':

    input_path = '../paper_figures/results/heterogeneous_ic2_net'

    """ load cluster data """

    node_array = np.load(
        '../paper_figures/results'
        '/clusters_funcnet_homogeneous_ic1_10s_no_noise/'
                         'ic_ic0/cluster_ic_ic0_funcnet_homogeneous_ic1_10s_no_noise.npy')

    """ generate plot """

    #node_array = np.load('Am-_ic2/clusters_Am-_10_0_ic2_ic0.npy')
    figure_name = 'clusters_Am-_25_0_ic2_ic21'
    plot_components_standalone(node_array, figure_name)







