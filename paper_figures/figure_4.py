# -*- coding: utf-8 -*-
""" Create figure 4 from the paper.

Part of the accompanying code for the paper "Exploring localization in
nonlinear oscillator systems through network-based predictions" by Charlotte
Geier and Norbert Hoffmann submitted to the Journal of Sound and Vibration in July 2024.

To reproduce the figure, run the code without changing it.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""


import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec

cm = 1 / 2.54
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

# initialize figure

fig = plt.figure()

""" setup figure structure """

outer = GridSpec(nrows=5, ncols=1,
                 left=0,
                 right=1,
                 bottom=0,
                 top=0.95,
                 figure=fig,
                 wspace=0.1,
                 hspace=0.2)

ax1 = fig.add_subplot(outer[0, 0])
ax2 = fig.add_subplot(outer[1, 0])

ax3 = fig.add_subplot(outer[2, 0])
ax4 = fig.add_subplot(outer[3, 0])
ax5 = fig.add_subplot(outer[4, 0])


""" do the actual plotting """

from plots.plot_in_degree import plot_in_degrees

# - uncertain parameters: in-degree
m_vars = np.load('results/funcnet_heterogeneous_ic1_10s_no_noise/m-_vars.npy')
means = np.load('results/degrees_funcnet_heterogeneous_ic1_10s_no_noise/degrees_funcnet_heterogeneous_ic1_10s_no_noise_means_cart_in.npy')
stds = np.load('results/degrees_funcnet_heterogeneous_ic1_10s_no_noise/degrees_funcnet_heterogeneous_ic1_10s_no_noise_stds_cart_in.npy')
plot_in_degrees(means, stds, m_vars, ax1,
                linewidth=1.5,
                xaxis_label=False,
                legend='legend_v2',
                ylims=[-0.2, 12],
                ylabel='$z_{\mathrm{in,pu},i}$')
ax1.set_xticks([])
print(f'First k=0 for data with uncertain pars at: m = {m_vars[np.where(means[3,:]==0)[0][0]]:.3f}.')

# - noise: in-degree
m_vars = np.load('results/funcnet_homogeneous_ic1_10s_added_noise/m-_vars.npy')
means = np.load('results/degrees_funcnet_homogeneous_ic1_10s_added_noise'
                '/degrees_funcnet_homogeneous_ic1_10s_added_noise_means_cart_in.npy')
stds = np.load('results/degrees_funcnet_homogeneous_ic1_10s_added_noise'
               '/degrees_funcnet_homogeneous_ic1_10s_added_noise_stds_cart_in.npy')
plot_in_degrees(means, stds, m_vars, ax2,
                linewidth=1.5,
                xaxis_label=False,
                ylims=[-0.2, 11],
                ylabel='$z_{\mathrm{in,noise},i}$')
ax2.set_xticks([])
print(f'First k=0 for noisy-data at: m = {m_vars[np.where(means[3,:]==0)[0][0]]:.3f}.')

# - mmt time series length: in-degree

# - 5 seconds length
m_vars = np.load('results/funcnet_homogeneous_ic1_5s_no_noise/m-_vars.npy')
means = np.load('results/degrees_funcnet_homogeneous_ic1_5s_no_noise'
                '/degrees_funcnet_homogeneous_ic1_5s_no_noise_means_cart_in.npy')
stds = np.load('results/degrees_funcnet_homogeneous_ic1_5s_no_noise'
               '/degrees_funcnet_homogeneous_ic1_5s_no_noise_stds_cart_in.npy')
plot_in_degrees(means, stds, m_vars, ax3,
                linewidth=1.5,
                xaxis_label=False,
                ylims=[-0.2, 11],
                ylabel='$z_{\mathrm{in,5s}, i}$')
ax3.set_xticks([])
print(f'First k<0.1 for 5s-data at: m = '
      f'{m_vars[np.where(means[3,:]<0.1)[0][0]]:.3f}.')

# - 25 seconds length
m_vars = np.load('results/funcnet_homogeneous_ic1_25s_no_noise/m-_vars.npy')
means = np.load('results/degrees_funcnet_homogeneous_ic1_25s_no_noise'
                '/degrees_funcnet_homogeneous_ic1_25s_no_noise_means_cart_in.npy')
stds = np.load('results/degrees_funcnet_homogeneous_ic1_25s_no_noise'
               '/degrees_funcnet_homogeneous_ic1_25s_no_noise_stds_cart_in.npy')
plot_in_degrees(means, stds, m_vars, ax4,
                linewidth=1.5,
                xaxis_label=False,
                ylims=[-0.2, 11],
                ylabel='$z_{\mathrm{in,25s}, i}$')
ax4.set_xticks([])
print(f'First k=0 for 25s-data at: m = {m_vars[np.where(means[3,:]==0)[0][0]]:.3f}.')
print(f'Peak of k_35 for 25s-data at: m = {m_vars[np.where(means[2,:]==max(means[2,20:80]))[0][0]]:.3f}.')

# - mmt time series length: clusters

from plots.plot_components import plot_components
node_array = np.load(
    'results/clusters_funcnet_homogeneous_ic1_25s_no_noise/ic_ic21'
    '/cluster_ic_ic21_funcnet_homogeneous_ic1_25s_no_noise.npy')
plot_components(node_array, ax5, plot_legend=True,
                ylabel='SCC 25s',
                settings='robustness',
                xlabel='$m_4$')
print(f'Cluster splits: node 3 at m = {m_vars[-71]:.3f}, nodes 2 and 4 at m = {m_vars[-38]:.3f}')

""" figure size and storing things """

width_, height_, resolution = 8.4, 12, 300
fig.set_size_inches(width_ * 0.3937,
                    height_ * 0.3937)  # this is only inches. convert cm to inch by * 0.3937007874
plt.savefig('figure_4_rev_1.png', dpi=resolution, bbox_inches="tight")
plt.show()

""" initial condition """
x0s = np.load('data/x0s_1.npy')
x0s[:, 21]


