# -*- coding: utf-8 -*-
""" Create figure 2 from the paper.

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
import networkx as nx
from matplotlib import patches, pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

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

outernmost = GridSpec(nrows=2, ncols=1,
                      left=0,
                      right=1,
                      bottom=0,
                      top=0.95,
                      figure=fig,
                      wspace=0.1,
                      hspace=0.25)
outer1 = GridSpecFromSubplotSpec(nrows=2, ncols=1,
                                 subplot_spec=outernmost[0],
                                 wspace=0.1,
                                 hspace=0.2)
outer2 = GridSpecFromSubplotSpec(nrows=2, ncols=1,
                                 subplot_spec=outernmost[1],
                                 wspace=0.1,
                                 hspace=0.2)
inner_1 = GridSpecFromSubplotSpec(nrows=1, ncols=4,
                                  subplot_spec=outer1[0,0],
                                  wspace=0.3 * cm,
                                  hspace=0)
ax11 = fig.add_subplot(inner_1[0, 0])
ax12 = fig.add_subplot(inner_1[0, 1])
ax13 = fig.add_subplot(inner_1[0, 2])
ax14 = fig.add_subplot(inner_1[0, 3])

inner_2 = GridSpecFromSubplotSpec(nrows=1, ncols=1,
                                  subplot_spec=outer1[1,0],
                                  wspace=0.3 * cm,
                                  hspace=0)
ax21 = fig.add_subplot(inner_2[0, 0])

inner_3 = GridSpecFromSubplotSpec(nrows=1, ncols=3,
                                  subplot_spec=outer2[0,0],
                                  wspace=0.3 * cm,
                                  hspace=0)
ax3 = fig.add_subplot(inner_3[0, 0:3])

inner_4 = GridSpecFromSubplotSpec(nrows=1, ncols=6,
                                  subplot_spec=outer2[1,0],
                                  wspace=0.3 * cm,
                                  hspace=0)
ax41 = fig.add_subplot(inner_4[0, 0:2])
ax42 = fig.add_subplot(inner_4[0, 2:4])
ax43 = fig.add_subplot(inner_4[0, 4:6])

""" line 1: plot time series data"""

from plots.plot_sectors import plot_sectors

n_sectors = 10
t = np.load('data/homogeneous_ic1/t.npy')

sol_1 = np.load('data/homogeneous_ic1/0.8/homogeneous_ic1_m0.8_ic0_c.npy')
plot_sectors(sol_1[:201, :], n_sectors, ax11,
             add_ticks=True,
             vmin=-1.5,
             vmax=1.5,
             x_ticks=[0, 100, 199],
             x_tick_labels=['0','5', '10'],
             y_ticks=[1,3,5,7,9],
             y_tick_labels=['2','4','6','8','10'],
             add_labels=True,
             move_ticks_to_top=True)

sol_2 = np.load('data/homogeneous_ic1/0.904/homogeneous_ic1_m0.904_ic36_c.npy')
plot_sectors(sol_2[:201, :], n_sectors, ax12,
             add_ticks='no_yticks',
             vmin=-1.5,
             vmax=1.5,
             x_ticks=[0, 100, 199],
             x_tick_labels=['0','5', '10'],
             y_ticks=[1,3,5,7,9],
             y_tick_labels=['2','4','6','8','10'],
             add_labels=False,
             move_ticks_to_top=True)

sol_3 = np.load('data/homogeneous_ic1/0.904/homogeneous_ic1_m0.904_ic0_c.npy')
plot_sectors(sol_3[:201, :], n_sectors, ax13,
             add_ticks='no_yticks',
             vmin=-1.5,
             vmax=1.5,
             x_ticks=[0, 100, 199],
             x_tick_labels=['0','5', '10'],
             y_ticks=[1,3,5,7,9],
             y_tick_labels=['2','4','6','8','10'],
             add_labels=False,
             move_ticks_to_top=True)

sol_4 = np.load('data/homogeneous_ic1/1.0/homogeneous_ic1_m1.0_ic0_c.npy')
plot_sectors(sol_4[:201, :], n_sectors, ax14,
             add_ticks='no_yticks',
             vmin=-1.5,
             vmax=1.5,
             x_ticks=[0, 100, 199],
             x_tick_labels=['0','5', '10'],
             add_labels=False,
             move_ticks_to_top=True)

""" line 2: plot in-degree data """

means = np.load('results/degrees_funcnet_homogeneous_ic1_10s_no_noise/degrees_funcnet_homogeneous_ic1_10s_no_noise_means_cart_in.npy')
stds = np.load('results/degrees_funcnet_homogeneous_ic1_10s_no_noise'
               '/degrees_funcnet_homogeneous_ic1_10s_no_noise_stds_cart_in.npy')
m_vars = np.load('results/funcnet_homogeneous_ic1_10s_no_noise/m-_vars.npy')

from plots.plot_in_degree import plot_in_degrees
plot_in_degrees(means, stds, m_vars, ax21,
                legend='legend_v1',
                linewidth=1.5)


""" line 3: plot clusters """

from plots.plot_components import plot_components
# to plot overview of cluster evolution for a specific ic
node_array = np.load(
    'results/clusters_funcnet_homogeneous_ic1_10s_no_noise/ic_ic1'
    '/cluster_ic_ic1_funcnet_homogeneous_ic1_10s_no_noise.npy')
plot_components(node_array, ax3, plot_legend=True, ylabel=True,
              settings='overview1')


""" line 4: plot exemplary networks """

from plots.plot_single_graph import plot_single_condensed_graph
node_size=100

path_to_nw = 'results/funcnet_homogeneous_ic1_10s_no_noise/0.8/Am-_m0.8_ic0/G_cartesian'
G_1 = nx.read_edgelist(path_to_nw, create_using=nx.DiGraph)
ssc = list(nx.strongly_connected_components(G_1))
G_c = nx.condensation(G_1, ssc)
plot_single_condensed_graph(G_c, nx.circular_layout(G_c), ax41, node_size=node_size,
                            node_color=['blue', 'tab:blue', 'red'])

path_to_nw = 'results/funcnet_homogeneous_ic1_10s_no_noise/0.9373737373737374/Am-_m0.9373737373737374_ic24/G_cartesian'
G_1 = nx.read_edgelist(path_to_nw, create_using=nx.DiGraph)
ssc = list(nx.strongly_connected_components(G_1))
G_c = nx.condensation(G_1, ssc)
plot_single_condensed_graph(G_c, nx.circular_layout(G_c), ax42, node_size=node_size,
                            node_color=['tab:blue', 'red'])

path_to_nw = 'results/funcnet_homogeneous_ic1_10s_no_noise/1.0/Am-_m1.0_ic24/G_cartesian'
G_1 = nx.read_edgelist(path_to_nw, create_using=nx.DiGraph)
ssc = list(nx.strongly_connected_components(G_1))
G_c = nx.condensation(G_1, ssc)
plot_single_condensed_graph(G_c, nx.circular_layout(G_c), ax43, node_size=node_size,
                            node_color='tab:blue')

""" add some arrows """

# top left arrow
transFigure = fig.transFigure.inverted()
coord1 = transFigure.transform(ax11.transData.transform([5/0.05,10]))
coord2 = transFigure.transform(ax21.transData.transform([0.801,11]))
arrow = patches.FancyArrowPatch(
    coord1,  # posA
    coord2,  # posB
    shrinkA=0,  # so tail is exactly on posA (default shrink is 2)
    shrinkB=0,  # so head is exactly on posB (default shrink is 2)
    transform=fig.transFigure,
    color="black",
    arrowstyle="<|-",  # "normal" arrow
    mutation_scale=10,  # controls arrow head size
    linewidth=1,
)
fig.patches.append(arrow)

# top 2nd arrow
coord1 = transFigure.transform(ax12.transData.transform([5/0.05,10]))
coord2 = transFigure.transform(ax21.transData.transform([0.903,11]))
arrow = patches.FancyArrowPatch(
    coord1,  # posA
    coord2,  # posB
    shrinkA=0,  # so tail is exactly on posA (default shrink is 2)
    shrinkB=0,  # so head is exactly on posB (default shrink is 2)
    transform=fig.transFigure,
    color="black",
    arrowstyle="<|-",  # "normal" arrow
    mutation_scale=10,  # controls arrow head size
    linewidth=1,
)
fig.patches.append(arrow)

# top 3rd arrow
coord1 = transFigure.transform(ax13.transData.transform([5/0.05,10]))
coord2 = transFigure.transform(ax21.transData.transform([0.903,11]))
arrow = patches.FancyArrowPatch(
    coord1,  # posA
    coord2,  # posB
    shrinkA=0,  # so tail is exactly on posA (default shrink is 2)
    shrinkB=0,  # so head is exactly on posB (default shrink is 2)
    transform=fig.transFigure,
    color="black",
    arrowstyle="<|-",  # "normal" arrow
    mutation_scale=10,  # controls arrow head size
    linewidth=1,
)
fig.patches.append(arrow)

# top right arrow
coord1 = transFigure.transform(ax14.transData.transform([5/0.05,10.5]))
coord2 = transFigure.transform(ax21.transData.transform([0.999,11]))
arrow = patches.FancyArrowPatch(
    coord1,  # posA
    coord2,  # posB
    shrinkA=0,  # so tail is exactly on posA (default shrink is 2)
    shrinkB=0,  # so head is exactly on posB (default shrink is 2)
    transform=fig.transFigure,
    color="black",
    arrowstyle="<|-",  # "normal" arrow
    mutation_scale=10,  # controls arrow head size
    linewidth=1,
)
fig.patches.append(arrow)

# bottom left
transFigure = fig.transFigure.inverted()
coord1 = transFigure.transform(ax3.transData.transform([10, -1.3]))
coord2 = transFigure.transform(ax3.transData.transform([1, -0.7]))
arrow = patches.FancyArrowPatch(
    coord1,  # posA
    coord2,  # posB
    shrinkA=0,  # so tail is exactly on posA (default shrink is 2)
    shrinkB=0,  # so head is exactly on posB (default shrink is 2)
    transform=fig.transFigure,
    color="black",
    arrowstyle="<|-",  # "normal" arrow
    mutation_scale=10,  # controls arrow head size
    linewidth=1,
)
fig.patches.append(arrow)

# bottom middle
transFigure = fig.transFigure.inverted()
coord1 = transFigure.transform(ax3.transData.transform([50, -1.3]))
coord2 = transFigure.transform(ax3.transData.transform([50, -0.7]))
arrow = patches.FancyArrowPatch(
    coord1,  # posA
    coord2,  # posB
    shrinkA=0,  # so tail is exactly on posA (default shrink is 2)
    shrinkB=0,  # so head is exactly on posB (default shrink is 2)
    transform=fig.transFigure,
    color="black",
    arrowstyle="<|-",  # "normal" arrow
    mutation_scale=10,  # controls arrow head size
    linewidth=1,
)
fig.patches.append(arrow)

# bottom right
transFigure = fig.transFigure.inverted()
coord1 = transFigure.transform(ax3.transData.transform([87, -1.3]))
coord2 = transFigure.transform(ax3.transData.transform([98, -0.7]))
arrow = patches.FancyArrowPatch(
    coord1,  # posA
    coord2,  # posB
    shrinkA=0,  # so tail is exactly on posA (default shrink is 2)
    shrinkB=0,  # so head is exactly on posB (default shrink is 2)
    transform=fig.transFigure,
    color="black",
    arrowstyle="<|-",  # "normal" arrow
    mutation_scale=10,  # controls arrow head size
    linewidth=1,
)
fig.patches.append(arrow)

""" figure size and storing things """

width_, height_, resolution = 8.4, 12, 300
fig.set_size_inches(width_ * 0.3937,
                    height_ * 0.3937)  # this is only inches. convert cm to inch by * 0.3937007874
plt.savefig('figure_2.png', dpi=resolution, bbox_inches="tight")
plt.show()


