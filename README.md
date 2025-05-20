# Code: Exploring localization in nonlinear oscillator systems through network-based predictions

Copyright (C) 2024  Charlotte Geier, Dynamics Group (M-14),
Hamburg University of Technology, Hamburg, Germany.
Contact:  [tuhh.de/dyn](https://www.tuhh.de/dyn)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

---
# Overview


Hi there! This repository contains the accompanying code for the 
paper "Exploring localization in nonlinear oscillator systems through 
network-based predictions" by C. Geier and N. Hoffmann published in Chaos 35 
(5) 2025 doi: 10.1063/5.0265366 . Available at https://arxiv.org/abs/2407.05497

You can use this code to reproduce the results presented in the paper, or to perform 
your own studies on functional networks! 
All computation is performed in pure Python.


**Reference**

Please acknowledge and cite the use of this software and its authors when results are used in publications or published elsewhere. You can use the following reference: 
> C. Geier: **Code for paper Exploring localization in nonlinear oscillator systems through network-based predictions** (v1.0). Zenodo. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12611988.svg)](https://doi.org/10.5281/zenodo.12611988)

---
# Prerequisites

The code in this repository was tested on 
- Ubuntu 20.04.6 running 
- PyCharm 2021.3.2 (Professional Edition)
- Python 3.8.12

Requirements are listed in 'requirements.txt' and can be installed via pip 
using `pip install -r requirements.txt`.

---
# Navigation

This code reprovies the following ressources: 
1. The possibilty of recreating the figures from data quickly, by using the 
   code and data provided in the directory paper_figures
2. The option of reproducing the results from scratch by using the code 
   provided as 
   1. data_generation
   2. network_computation
   3. compute_components
   4. compute_in_degrees
3. The option to compute functional networks from other datasets by using 
   the network_computation file on own data (more info below).


### 1. To reproduce figures:
use figure_2-4.py in paper_figures 

### 2. To reproduce results from scratch:
**data generation:**
- run data_generation.py to create
  - initial conditions
  - integration time vector
  - three data sets used in the paper
    1. homogeneous_ic1: homogeneous system, x0 in [0, 0.1] (-> Figure 2)
    2. homogeneous_ic2: homogeneous system, x0 in [0, 0.01] (-> Figure 3)
    3. heterogeneous_ic1: heterogeneous system, x0 in [0, 0.1] (-> Figure 4)
  -> stores data and figures in data/ TODO: rename to data_test back to data
        
**functional network computation:**
- run network_computation to compute functional networks from given dataset
  - script will loop over the data in the directory defined by 
    data_directory_main and create functional networks for each

**analyses:**
- to compute strongly connected components within networks,
  run compute_components.py
  - for one exemplary initial condition, over a parameter variation (-> Figs 
    2-4)
  - for one specific value of a parameter and a set of initial conditions 
    (not in paper, but useful for analysis)
- to compute in-degrees within networks, rum compute_in_degrees.py

### 3. To compute a functional network from your own data:
run 
  - compute_functional_network(your_data, rr=(0.03, 0.03, 0.02))
    where your_data = np.array[n_timesteps, 2*n_variables] for 2nd order system
  - or compute_functional_network(your_data, rr=(0.03, 0.03, 0.02), 
    n=n_variables)
    where your_data = np.array[n_timesteps, n_variables] for 1st order system
  
