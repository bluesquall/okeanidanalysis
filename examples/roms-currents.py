#!/usr/bin/env python
"""
`roms-currents.py`
==================
An example script to plot currents from Regional Ocean Modeling System (ROMS) 
on a map of the area around Monterey Bay.

"""

# import oceanidanalysis as oa
from pydap.client import open_url

from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def open_roms(url, tidx = -1, zbin = 0, verbosity = 0):
    """Get specified current layer from ROMS opendap netCDF file."""
    dataset = open_url(url)
    if verbosity > 0: print 'dataset: ', dataset.name
    t_rel = float(np.array(dataset['time'][tidx]).squeeze())
    print t_rel, type(t_rel)
#    the units & label are different for nowcast & forecast
#    t_start_l = dataset['time'].attributes['units'].split()[2].split('-')
#    t_start_l.extend(dataset['time'].attributes['units'].split()[3].split(':'))
#    t_start = datetime(*t_start_l)
    print dataset['time'].attributes['units']
    tstr = ('T'.join(dataset['time'].attributes['units'].split()[2:4]))
    t_start = datetime.strptime(tstr,'%Y-%m-%dT%H:%M:%S')
    ts = t_start + timedelta(t_rel) # in days... make more portable...
    t = np.float(ts.strftime('%s.%f'))
    u = np.array(dataset['u'][tidx,zbin,:,:]).squeeze()
    v = np.array(dataset['v'][tidx,zbin,:,:]).squeeze()
    lat = np.array(dataset['lat'])
    lon = np.array(dataset['lon'])
    lon[lon > 180] -= 360

    depth = np.array(dataset['depth'][zbin])[0]

    if verbosity > 0:
        print 'max |u|:', u.__abs__().max()
        print 'max |v|:', v.__abs__().max()

#    fig = plt.figure(); ax = fig.add_subplot(1,1,1); ax.contourf(u)

    u[u < -9e3] = np.nan
    v[v < -9e3] = np.nan

    if verbosity > 0:
        print 'max |u|:', u[~np.isnan(u)].__abs__().max()
        print 'max |v|:', v[~np.isnan(v)].__abs__().max()


        print 't:', t/60.0

    return t, lat, lon, depth, u, v

#TODO a method to construct the proper url...


def draw_monterey_bay():
    m = Basemap(lat_0 = 36.75, lon_0 = -121.0, 
        llcrnrlat = 36, llcrnrlon = -122.8, 
        urcrnrlat = 37, urcrnrlon = -121.75, 
        resolution = 'f',
        )
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')
    m.drawrivers(color='b')
    m.drawparallels(np.arange(36,37,0.1),labels=[1,0,0,0],fontsize=8)
    m.drawmeridians(np.arange(-122.8,-120,0.1),labels=[0,0,0,1],fontsize=8)
    return m


def main(url, outfile=None, zbin=0, verbosity=0):
    m = draw_monterey_bay()
    plt.hold(True)
    t, latitudes, longitudes, depth, u, v = open_roms(url, 0, zbin, verbosity)
    print 'depth: ', depth, ' [meters]'

    n = 24 # number of points in output grid on map
        #TODO make this dependent on hte resolution of the input data?
    um, vm, xm, ym = m.transform_vector(u, v, longitudes, latitudes, 
        round(len(longitudes)/4), round(len(latitudes)/4), 
        returnxy=True, masked=True, order=1)
    ulevels = np.arange(0,0.51,0.01)
    m.contourf(xm,ym,(um**2 + vm**2)**0.5, ulevels)
    m.colorbar()
    q = m.quiver(xm,ym,um,vm,scale=None)
    qk = plt.quiverkey(q, 0.1, -0.2, 1, '1 m/s', labelpos='W')

    lfn = url.rsplit('/')[-1].replace('_','\_')
    ts = datetime.utcfromtimestamp(t).isoformat()
    plt.title(r'ROMS: {0}Z, {1} m depth'.format(ts, depth))
    
    if outfile: plt.savefig(outfile) #TODO save args...
    else: plt.show()    


if __name__ == "__main__":
    
    url = 'http://ourocean.jpl.nasa.gov:8080/thredds/dodsC/MBNowcast/mb_das_2012091715.nc'
#    url = 'http://ourocean.jpl.nasa.gov:8080/thredds/dodsC/MBForecast/mb_fcst_2012091703.nc'
    main(url, zbin=5, verbosity=1)

    
