# -*- coding: utf-8 -*-
""" Helper functions

Part of the accompanying code for the paper "Exploring localization in
nonlinear oscillator systems through network-based predictions" by Charlotte
Geier and Norbert Hoffmann submitted to the Journal of Sound and Vibration in July 2024.

Copyright (c) Charlotte Geier
Hamburg University of Technology, Dynamics Group
www.tuhh.de/dyn
charlotte.geier@tuhh.de

Licensed under the GPLv3. See LICENSE in the project root for license information.

30.06.2024
"""


def common_elements(list1, list2):
    """
    Find the common elements of two lists. Especially also helpful when looking at lists of lists,
    where intersection() fails.
    :param list1: a list
    :param list2: a second list
    :return: common elements of the two lists
    """
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result



def get_settings(name, dict):
    """
    Unpack parameter settings for Duffing oscillator from json file.

    :param name: name of parameter set
    :param dict: dictionary with parameter settings
    :return: m, alpha, beta, kl, knl, kc, F, Omega
    """

    from operator import itemgetter

    d_name = dict.pop(name)
    m, alpha, beta, kl, knl, kc, F, Omega = itemgetter('m', 'alpha', 'beta', 'kl', 'knl', 'kc', 'F', 'Omega')(d_name)

    return m, alpha, beta, kl, knl, kc, F, Omega


def load_json(path_to_json):
    """
    Load a JSON file from a given location
    :param path_to_json: path to json file
    :return: json_data a dictionary containing the contents of the json

    """

    import json

    with open(path_to_json, 'r') as file:
        json_data = json.load(file)

    return json_data

