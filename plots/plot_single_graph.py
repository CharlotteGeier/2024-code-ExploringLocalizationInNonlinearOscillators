# -*- coding: utf-8 -*-
""" Plot a single functional network.

Part of the accompanying code for the paper "Exploring localization in
nonlinear oscillator systems through network-based predictions" by Charlotte
Geier and Norbert Hoffmann submitted to the Journal of Sound and Vibration in July 2024.

Either in full, or condensed version.
Input a functional network.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024

"""

import networkx as nx
import matplotlib.pyplot as plt

def plot_single_graph(G, ax, pos, communities=None, **kwargs):
    " Plot a single graph in a specific location ax"

    color = kwargs.get('color','black')
    edgecolor = kwargs.get('edgecolor','tab:blue')
    labels = kwargs.get('labels', {"0":1, "1":2, "2":3, "3":4 , "4":5, "5":6, "6":7, "7":8, "8":9 , "9":10})
    node_size = kwargs.get('node_size',160)
    remove_edges = kwargs.get('remove_edges')
    margins = kwargs.get('margins', 0.1)
    label_font_size=kwargs.get('label_font_size',7)
    arrow_size=kwargs.get('arrow_size',5)
    alpha = 0.8

    # in all cases, draw nodes and edges, except when there's only one edge: only draw one big node
    if remove_edges:
        nx.draw_networkx_nodes(G,
                               ax=ax,
                               pos=pos,
                               node_color=[color],
                               node_size=500,
                               alpha=alpha,
                               margins=margins
                               )
    else:
        if communities:
            #creates a range of unique colors corresponding to the number of SSC
            unique_colors = range(len(communities))
            node_colors = []
            #loop over all the nodes
            for node in G.nodes():
                #loop over ssc and its indices
                for i, comm in enumerate(communities):
                    #check if the node is part of the ssc
                    if node in comm:
                        #if yes color the node (color repeat cyclicly if there are more nodes in unique_colors)
                        node_colors.append(unique_colors[i % len(unique_colors)])
            nx.draw_networkx_nodes(G, ax=ax,
                                   pos=pos,
                                   node_color=node_colors,
                                   cmap=plt.get_cmap('viridis'),
                                   node_size=node_size,
                                   alpha=alpha,
                                   margins=margins,
                                   edgecolors=node_colors)
            nx.draw_networkx_edges(G,
                                   ax=ax,
                                   pos=pos,
                                   width=1,
                                   edge_color=edgecolor,
                                   alpha=alpha,
                                   arrowsize=arrow_size,
                                   node_size=node_size)

        else:
              nx.draw_networkx_nodes(G,
                                     ax=ax,
                                     pos=pos,
                                     node_color=color,
                                     node_size=node_size,
                                     alpha=alpha,
                                     margins=margins,
                                     edgecolors=edgecolor)
              nx.draw_networkx_edges(G,
                                     ax=ax,
                                     pos=pos,
                                     width=1,
                                     edge_color=edgecolor,
                                     alpha=alpha,
                                     arrowsize=arrow_size,
                                     node_size=node_size)
    if labels == 'dont_change':
        # keep original node labels
        nx.draw_networkx_labels(G,
                                ax=ax,
                                pos=pos,
                                font_size=label_font_size,
                                font_family='serif',
                                font_color='Black')
    else:
    # overwrite labels s.t. they go from 1 to 5 instead of 0 to 4
     nx.draw_networkx_labels(G,
                             ax=ax,
                             labels={n:lab for n,lab in labels.items() if n in pos},
                             pos=pos,
                             font_size=label_font_size,
                             font_family='serif',
                             font_color='Black')


def plot_single_condensed_graph(G_condensed, pos, ax, **kwargs):
    """
    Plot a single condensed graph.
    Uses plot single graph and adjusts the labels to show which nodes are condensed
    together
    :param G_condensed:
    :param pos:
    :param ax:
    :param kwargs:
    :return:
    """

    node_size = kwargs.get('node_size', 1500)
    node_color = kwargs.get('node_color', 'tab:blue')

    # generate new labels
    node_data = G_condensed.nodes.data()
    labels = {}

    for new_node in node_data:
        # for debugging: print node info
        # print(f'{new_node}')

        # maybe for future reference: labels[new_node[0]] = int(new_node[1]['members'].pop())
        labels[new_node[0]] = sorted(list(new_node[1]['members']))

    plot_single_graph(G_condensed,
                      pos=pos,
                      ax=ax,
                      color=node_color,
                      #labels=labels,
                      label_font_size=12,
                      arrow_size=20,
                      node_size=node_size)
    ax.set_xticks([])
    ax.set_yticks([])



if __name__ == '__main__':



    # define graph location
    path_to_nw = '../paper_figures/results/funcnet_homogeneous_ic1_10s_no_noise/0.8' \
                 '/Am' \
                 '-_m0.8_ic0/G_cartesian'

    #
    G = nx.read_edgelist(path_to_nw,
                               create_using=nx.DiGraph)

    pos = nx.circular_layout(G)

    cm = 1/2.54

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6*cm,6*cm))
    plot_single_graph(G, pos=pos, ax=ax,
                      color='black',
                      arrow_size=10,
                      node_size=200,
                      label_font_size=10)
    #plt.savefig('net.jpg',dpi=600)
    plt.show()

