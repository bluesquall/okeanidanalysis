#!/usr/bin/env python
"""
monterey-bay-map.py
-------------------

An example script to generate a map of the area around Monterey Bay.

"""

# import oceanidanalysis as oa
from urllib import urlretrieve
from netCDF4 import Dataset

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def open_nc_ss(url):
    """Grab data from a NetCDF Subset Service for Grids."""
    ncfile, header = urlretrieve(url)   
    data = Dataset(ncfile)
    return data

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
    m.drawparallels(np.arange(36,37,0.1),labels=[1,1,0,0],fontsize=10)
    m.drawmeridians(np.arange(-123,-120,0.1),labels=[0,0,1,1],fontsize=10)
    return m

def main(url, outfile=None):
    m = draw_monterey_bay()
    plt.hold(True)
    data = open_nc_ss(url)

#    print data.summary

#    print data.geospatial_lat_min
#    print data.geospatial_lat_max
#    print data.geospatial_lon_min
#    print data.geospatial_lon_max
    
    latitudes = data.variables['lat']#[::-1]
      # optionally slice to reverse latitudes so they go from south to north.
    longitudes = data.variables['lon']
    print data.variables['water_u'].shape
    print latitudes.shape
    print longitudes.shape

   
    u = data.variables['water_u'][0].squeeze()
    v = data.variables['water_v'][0].squeeze()
#    u = data.variables['u'].squeeze()
#    v = data.variables['v'].squeeze()
        # first dimension is time, just grab the first part of the dataset...

    

#    fig = plt.figure(100)
#    ax = fig.add_subplot(1,2,1)
#    ax.plot(latitudes)
#    ax = fig.add_subplot(1,2,2)
#    ax.plot(longitudes)
#    fig = plt.figure(101)
#    ax = fig.add_subplot(1,1,1)    
#    ax.contour(u)
#    for ui in u: 
#        plt.plot(ui)
#        print ui

    n = 64 # number of points in output grid on map
        #TODO make this dependent on hte resolution of the input data?
    um, vm, xm, ym = m.transform_vector(u, v, longitudes, latitudes, 
        n, n, returnxy=True, masked=True, order=1)
    q = m.quiver(xm,ym,um,vm,scale=None)
#    print um
#    qk = plt.quiverkey(q, 0.1, 0.1, 1, '1 m/s', labelpos='W')
    
    if outfile: plt.savefig(outfile) #TODO save args...
    else: plt.show()
    
    


if __name__ == "__main__":
    
#    url = 'http://hfrnet.ucsd.edu/thredds/ncss/grid/HFRNet/USWC/1km/hourly/RTV?var=u,v&north=37&south=36.5&east=-121.75&west=-122.5&time_start=2012-09-12T12:00:00Z&time_end=2012-09-12T13:00:00Z&accept=application/x-netcdf'
#    url = 'http://hfrnet.ucsd.edu/thredds/ncss/grid/HFRNet/USWC/1km/hourly/RTV?var=u,v&time_start=2012-09-10T12:00:00Z&time_end=2012-09-12T13:00:00Z&accept=application/x-netcdf'
    url = 'http://cencalcurrents.org/DataRealTime/Gnome/MNTY/2012_09/GNOME_MNTY_2012_09_13_2300.nc'
    #TODO write class/methods to generate these in a flexible but robust way, put them in oceanidanalysis package
    main(url)

    
