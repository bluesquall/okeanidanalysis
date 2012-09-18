#!/usr/bin/env python
"""
monterey-bay-map.py
-------------------

An example script to generate a map of the area around Monterey Bay.

"""

# import oceanidanalysis as oa
from urllib import urlretrieve
from netCDF4 import Dataset

from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

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
    return t, lat, lon, z, u, v


def draw_monterey_bay():
    m = Basemap(lat_0 = 36.75, lon_0 = -121.0, 
        llcrnrlat = 36.5, llcrnrlon = -122.5, 
        urcrnrlat = 37, urcrnrlon = -121.75, 
        resolution = 'f',
        )
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')
    m.drawrivers(color='b')
    m.drawparallels(np.arange(36,37,0.1),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(-123,-120,0.1),labels=[0,0,0,1],fontsize=10)
    return m


def main(url, outfile=None):
    m = draw_monterey_bay()
    plt.hold(True)
    t, latitudes, longitudes, z, u, v = open_hfr(url)

    u = u.squeeze()
    v = v.squeeze()

    n = 64 # number of points in output grid on map
        #TODO make this dependent on hte resolution of the input data?
    um, vm, xm, ym = m.transform_vector(u, v, longitudes, latitudes, 
        2*len(longitudes), 2*len(latitudes), 
        returnxy=True, masked=True, order=1)
    ulevels = np.arange(0,0.51,0.01)
    m.contourf(xm,ym,(um**2 + vm**2)**0.5, ulevels)
    m.colorbar()
    q = m.quiver(xm,ym,um,vm,scale=None)
    qk = plt.quiverkey(q, 0.1, -0.2, 1, '1 m/s', labelpos='W')
    
    plt.title('hfrnet 2km {}Z'.format(datetime.utcfromtimestamp(t).isoformat()))
    

    if outfile: plt.savefig(outfile) #TODO save args...
    else: plt.show()    


if __name__ == "__main__":
    
    url = 'http://hfrnet.ucsd.edu/thredds/ncss/grid/HFRNet/USWC/2km/hourly/RTV?var=u,v&north=37&south=36.5&east=-121.75&west=-122.5&time_start=2012-09-17T22:00:00Z&time_end=2012-09-18T23:00:00Z&accept=application/x-netcdf'
#    url = 'http://cencalcurrents.org/DataRealTime/Gnome/MNTY/2012_09/GNOME_MNTY_2012_09_17_2300.nc'
    #TODO write class/methods to generate these in a flexible but robust way, put them in oceanidanalysis package
    main(url)

    
