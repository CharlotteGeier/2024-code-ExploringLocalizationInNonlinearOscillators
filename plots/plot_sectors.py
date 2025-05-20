# -*- coding: utf-8 -*-
""" Plot time series data

Part of the accompanying code for the paper "Exploring localization in nonlinear oscillator systems through 
network-based predictions" by C. Geier and N. Hoffmann published in Chaos 35 
(5) 2025 doi: 10.1063/5.0265366 . Available at https://arxiv.org/abs/2407.05497

Input time vector and time series data.
Use standalone version for standalone plot.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024

"""

import numpy as np
from matplotlib import pyplot as plt


def plot_sectors(x, n_sectors, ax, **kwargs):

    interpolation = kwargs.get('interpolation', 'none')
    title = kwargs.get('title', False)
    vmin = kwargs.get('vmin', False)
    vmax = kwargs.get('vmax')
    add_ticks = kwargs.get('add_ticks', False)
    x_ticks = kwargs.get('x_ticks')
    x_tick_labels = kwargs.get('x_tick_labels')
    y_ticks = kwargs.get('y_ticks')
    y_tick_labels = kwargs.get('y_tick_labels')
    add_labels = kwargs.get('add_labels', True)
    move_ticks_to_top = kwargs.get('move_ticks_to_top', False)

    if vmin:
        im = ax.imshow(np.transpose(x[:, :n_sectors]),
                   aspect='auto',
                   interpolation=interpolation,
                   vmin=vmin,
                   vmax=vmax)
    else:
        im = ax.imshow(np.transpose(x[:, :n_sectors]),
                   aspect='auto',
                   interpolation=interpolation)

    if add_labels:
        ax.set_ylabel('oscillator')
        ax.set_xlabel('t\,[s]')


    if add_ticks == True:
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_tick_labels)
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_tick_labels)
    elif add_ticks == 'no_yticks':
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_tick_labels)
        ax.set_yticks([])
    if move_ticks_to_top:
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
    if title:
        plt.title(title)


def plot_sectors_standalone(x, n_sectors, **kwargs):
    """
    Plot movement in a chain of oscillators in color code. Yaxis represents sectors or individual oscillators,
    xaxis time, and color the amplitude of the oscillation.
    :param x: Time evolution, in n_timesteps x n_sectors, or n_timesteps x 2*n_sectors
    :param n_sectors: number of sectors to plot
    :kwargs: interpolation: whether or not to interpolate between values. matplotlib standard is 'antialiased',
    here 'none' is given as the default, as it provides a precise visualization of the data in the matrix.
    :return:
    """

    figsize = kwargs.get('figsize', (5, 2))
    showfig = kwargs.get('showfig', False)
    closefig = kwargs.get('closefig', False)

    # get saving info
    savefig = kwargs.get('savefig', False)
    figure_path = kwargs.get('figure_path', 'test_figure.pdf')

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

    fig, ax = plt.subplots(1, 1, figsize=figsize)
    plot_sectors(x, n_sectors, ax, kwargs=kwargs)
    plt.tight_layout()

    if savefig:
        plt.savefig(figure_path, dpi=500)

    if showfig:
        plt.show()

    if closefig:
        plt.close(fig)



if __name__ == '__main__':

    import numpy as np

    plt.rcParams.update({'font.size': 10,
                         'axes.labelsize': 10})
    cm = 1/2.54

    t = np.load('../paper_figures/data/homogeneous_ic1/t.npy')
    sol = np.load('../paper_figures/data/homogeneous_ic1/1.0/homogeneous_ic1_m1.0_ic0_c'
                  '.npy')
    n_sectors = 10

    plot_sectors_standalone(sol, n_sectors,
                            figsize=(5*cm, 5*cm),
                            add_ticks=True,
                            x_ticks=[0, 199],
                            x_tick_labels=['0', '10'],
                            y_ticks=[1, 3, 5, 7, 9],
                            y_tick_labels=['2', '4', '6', '8', '10'],
                            savefig=False,
                            closefig=False,
                            showfig=True,
                            figure_path='time_series.jpg')
