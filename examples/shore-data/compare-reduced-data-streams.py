#!/usr/bin/env python
#
# An example script to compare reduced data streams sent to shore.

import numpy as np
import matplotlib.pyplot as plt

import okeanidanalysis as oa

expressfile = "/Users/squall/Desktop/daphne-bin-logs/20150310T204202/shore.mat" 
priorityfile = "/Users/squall/Desktop/daphne-bin-logs/20150310T204202/cell-Priority.mat"
normalfile = "/Users/squall/Desktop/daphne-bin-logs/20150310T204202/cell-Normal.mat"
fullfile = None

files_to_compare, slate = [], []
if expressfile is not None:
    files_to_compare.extend(expressfile)
    slate.extend(oa.logs.OkeanidLog(expressfile))
if priorityfile is not None:
    files_to_compare.extend(priorityfile)
    slate.extend(oa.logs.OkeanidLog(priorityfile))
if normalfile is not None:
    files_to_compare.extend(normalfile)
    slate.extend(oa.logs.OkeanidLog(normalfile))
if fullfile is not None:
    files_to_compare.extend(fullfile)
    slate.extend(oa.logs.OkeanidLog(fullfile))
number_of_streams = len(files_to_compare)


# define a timeseries to compare on
dt = 10
t_start, t_end = slate[-1]['depth/time'][[0,-1]]
t_total = t_end - t_start
t = np.arange(t_start, t_end, dt)

# calculate the size and average bitrate of each stream (# of samples, # of bytes with timestamps)
sizeof_serialized_float = 8 # assume single-precision float
sizeof_serialized_timestamp = 8 # assume single-byte timestamp, but this might be wrong
sizeof_serialized_sample = sizeof_serialized_float + sizeof_serialized_timestamp

n_D = [len(s['depth/time']) for s in slate]
n_chl, n_T, n_S = [], [], []
for s in slate:
    try: 
        n_chl_ = len(s['WetLabsBB2FL/bin_mean_mass_concentration_of_chlorophyll_in_sea_water/time'])
    except:
        n_chl_ = len(s['mass_concentration_of_chlorophyll_in_sea_water/time'])
    n_chl.extend(n_chl_)
    try: 
        n_T_ = len(s['CTD_NeilBrown/bin_mean_sea_water_temperature/time'])
    except:
        n_T_ = len(s['sea_water_temperature/time'])
    n_T.extend(n_T_)
    try: 
        n_S_ = len(s['CTD_NeilBrown/bin_mean_sea_water_salinity/time'])
    except:
        n_S_ = len(s['sea_water_salinity/time'])
    n_S.extend(n_S_)

br_D = n_D / t_total
br_chl = n_chl / t_total
br_T = n_T / t_total
br_S = n_S / t_total

# plot comparisons








