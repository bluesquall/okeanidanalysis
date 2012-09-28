#!/usr/bin/env python
"""
monterey-bay-map.py
-------------------

An example script to generate a map of the area around Monterey Bay.

"""

import oceanidanalysis as oa
from urllib import urlretrieve
from netCDF4 import Dataset

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap

def open_hfr(url, verbosity = 0):
    """wrapper to choose appropriate netCDF opener."""
    try:
        t, lat, lon, z, u, v = open_hfrnet_thredds_nc_ss(url, verbosity)
    except KeyError: # the cencalcurrents netCDF has different labels
        t, lat, lon, z, u, v = open_ccc_gnome_nc(url, verbosity)
    except:
        raise Exception('can only open netCDF datasets from hfrnet or cencalcurrents, not ' + url)
    return t, lat, lon, z, u, v


def open_hfrnet_thredds_nc_ss(url, tidx = -1, verbosity = 0):
    """Grab data from a NetCDF Subset Service for Grids."""
    ncfile, header = urlretrieve(url)   
    data = Dataset(ncfile)
    if verbosity > 0: print data.summary 
    t = data.variables['time'][tidx]
    lat = data.variables['lat']
    lon = data.variables['lon']
    z = 0
    u = data.variables['u'][tidx]
    v = data.variables['v'][tidx]
    u = u.squeeze()
    v = v.squeeze()
    return t, lat, lon, z, u, v


def open_ccc_gnome_nc(url, tidx = -1, verbosity = 0):
    """Grab data from a CenCalCurrents GNOME NetCDF file."""
    ncfile, header = urlretrieve(url)   
    data = Dataset(ncfile)
    t = data.variables['time'][tidx]
    lat = data.variables['lat']
    lon = data.variables['lon']
    z = 0
    u = data.variables['water_u'][tidx]
    v = data.variables['water_v'][tidx]
    u = u.squeeze()
    v = v.squeeze()
    return t, lat, lon, z, u, v


def draw_monterey_bay():
    m = oa.maps.MontereyBay(resolution = 'f')
    m.drawcoastlines()
    m.drawdefault()
    m.drawgrid()
    return m 


def main(url, outfile=None, outdir=None):
    m = draw_monterey_bay()
    plt.hold(True)
#    t, latitudes, longitudes, z, u, v = open_hfr(url)
#    m.draw_currents(t, latitudes, longitudes, z, u, v)
    m.draw_currents(*open_hfr(url))

    t = m.timestamp['currents']
    title = 'hfrnet 6km {}Z'.format(datetime.utcfromtimestamp(t).isoformat())
    plt.title(title)
    
    if outfile: plt.savefig(outfile) #TODO save args...
    if outdir: plt.savefig(os.path.join(outdir,title.replace(' ','_').replace(':','') + '.png'), dpi=1200)
    else: plt.show()    

if __name__ == "__main__":
    
    url = 'http://hfrnet.ucsd.edu/thredds/ncss/grid/HFRNet/USWC/6km/hourly/RTV?var=u,v&north=37&south=35&east=-121&west=-123&time_start=2012-09-19T06:00:00Z&time_end=2012-09-19T06:00:01Z&accept=application/x-netcdf'
#    url = 'http://cencalcurrents.org/DataRealTime/Gnome/MNTY/2012_09/GNOME_MNTY_2012_09_17_2300.nc'
    #TODO write class/methods to generate these in a flexible but robust way, put them in oceanidanalysis package
#    main(url, outdir='/tmp')
    main(url)

