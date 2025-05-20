# -*- coding: utf-8 -*-
""" Plot evolution of node in degree in network.

Part of the accompanying code for the paper "Exploring localization in nonlinear oscillator systems through 
network-based predictions" by C. Geier and N. Hoffmann published in Chaos 35 
(5) 2025 doi: 10.1063/5.0265366 . Available at https://arxiv.org/abs/2407.05497

Input mean and standard deviation of node degree, computed via
compute_in_degrees.py.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024

"""

import numpy as np
from matplotlib import pyplot as plt

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

def plot_in_degrees(means, stds, m_vars, ax, **kwargs):

    alpha = kwargs.get('alpha', .1)
    linewdith = kwargs.get('linewidth', .5)
    legend = kwargs.get('legend')
    ylims = kwargs.get('ylims',[-0.2, 11.5])
    xaxis_label = kwargs.get('xaxis_label', True)
    ylabel = kwargs.get('ylabel', '$z_{\mathrm{in},i}$')

    for i in range(np.shape(means)[0]):
        if i == 3:
            ax.plot(m_vars, means[i, :],'-', label=f'$z_{i + 1}$', linewidth=linewdith)
            ax.fill_between(m_vars, means[i, :] - stds[i, :], means[i, :] + stds[i, :], alpha=alpha)
        elif i == 2:
            ax.plot(m_vars, means[i, :],':', label=f'$z_{i + 1}$', linewidth=linewdith)
            ax.fill_between(m_vars, means[i, :] - stds[i, :], means[i, :] + stds[i, :], alpha=alpha)
        elif i == 4:
            ax.plot(m_vars, means[i, :], ':', label=f'$z_{i + 1}$', linewidth=linewdith)
            ax.fill_between(m_vars, means[i, :] - stds[i, :], means[i, :] + stds[i, :], alpha=alpha)
        elif i == 9:
            ax.plot(m_vars, means[i, :], '--', label='$z_{10}$', linewidth=linewdith)
            ax.fill_between(m_vars, means[i, :] - stds[i, :], means[i, :] + stds[i, :], alpha=alpha)
        else:
            ax.plot(m_vars, means[i, :], '--', label=f'$z_{i + 1}$', linewidth=linewdith)
            ax.fill_between(m_vars, means[i, :] - stds[i, :], means[i, :] + stds[i, :], alpha=alpha)


    ax.set_ylim(ylims)
    ax.set_xlim([0.8, 1])
    if legend == 'legend_v0':
        ax.legend(bbox_to_anchor=(1, 1))
    elif legend == 'legend_v1':
        ax.legend(ncols=10,
                  columnspacing=0.1,
                  borderpad=0.1,
                  handlelength=1,
                  labelspacing=0.1,
                  loc='upper left')
    elif legend == 'legend_v2':
        ax.legend(ncols=10,
                  columnspacing=0.1,
                  borderpad=0.1,
                  handlelength=1,
                  labelspacing=0.1,
                  loc='upper left')

    ax.set_ylabel(ylabel)

    if xaxis_label:
        ax.set_xlabel('$m_4$')


if __name__ == '__main__':

    m_vars = np.load('../paper_figures/results/funcnet_heterogeneous_ic1_10s_no_noise/m-_vars.npy')
    means = np.load('../paper_figures/results'
        '/degrees_funcnet_heterogeneous_ic1_10s_no_noise/degrees_funcnet_heterogeneous_ic1_10s_no_noise_means_cart_in.npy')
    stds = np.load('../paper_figures/results/degrees_funcnet_heterogeneous_ic1_10s_no_noise'
                   '/degrees_funcnet_heterogeneous_ic1_10s_no_noise_stds_cart_in.npy')

    fig, ax = plt.subplots(1,1,figsize=(3,3))
    plot_in_degrees(means, stds, m_vars, ax)

    # figure export setup (size, resolution) (84mm or 174 mm width)
    width_, height_, resolution = 8.4, 5.5, 300
    fig.set_size_inches(width_ * 0.3937,
                        height_ * 0.3937)  # this is only inches. convert cm to inch by * 0.3937007874

    # figure export as impage and png image of certain size and resolution
    # plt.savefig("in_degree_25.png", dpi=resolution,
    #             bbox_inches="tight")  # bbox_inches takes care of keeping everything inside the frame that is being exported

    plt.show()