"""
oceanidanalysis.logs
====================

Generally useful methods that span across submodules.

"""

import numpy as np
import scipy as sp
import h5py
import matplotlib.pyplot as plt

class OceanidLog(h5py.File):

    def plot_timeseries(self, x, **kw):
        "A convenience function for plotting time-series."""
        plt.plot_date(self[x]['time'][:], self[x]['value'][:], **kw)
        # TODO  let it accept ax as an optional argument

    def map_trajectory(self, mapobject, **kw)
        lats = rad2deg(self['latitude']['value'][:])
        lons = rad2deg(self['longitude']['value'][:])
        x, y = mapobject(lons, lats)
        mapobject.plot(x, y, **kw)

    
