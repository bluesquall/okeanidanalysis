#!/usr/bin/env python
"""
`hf-radar-surface-currents.py`
------------------------------

An example script to generate a surface current map of Monterey Bay.

"""
import os
from datetime import datetime
from urllib import urlretrieve
import h5py
from netCDF4 import Dataset

import numpy as np
import scipy as sp
import scipy.io
import scipy.interpolate
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import oceanidanalysis as oa

#TODO make a wrapper -- at least for OMA -- that opens & concatenates data based on time windows
#XXX probably implement this as a class `Current` with subclasses url generators, and data readers for each source

def unravel_oma(lat, lon, z, glat=None, glon=None, returnxy=False):
    """Unravel variable y onto a lat/lon grid."""
    #TODO remove nans in oma data, too
    if not glat: glat = np.unique(lat) #TODO ensure monotonic and equally spaced
    if not glon: glon = np.unique(lon) #TODO ensure monotonic and equally spaced
#    gz = mlab.griddata(lon, lat, z, glon, glat)
    gz = sp.interpolate.griddata((lon, lat), z, np.meshgrid(glon, glat), method='nearest')
    #TODO using griddata for this is overkill, and may not be sustainable in the future -- write a more specific replacement that will handle missing values as masked _or_ nan, probably using np.ravel_multi_index
    if returnxy: return gz, glat, glon
    else: return gz
    #TODO move the function above to oa.lib

def ravel_oma(gx, gy, gz):
    """Complementary function -- important for generating rows in EOF analysis.

    """
    if gx.squeeze().ndim == 1: gx, gy = np.meshgrid(gx, gy)
    #TODO simpler treatment if inputs are masked arrays?
    z = gz.ravel()
    x = gx.ravel()[~isnan(z)]
    y = gy.ravel()[~isnan(z)]
    return x, y, z[~isnan(z)]

def open_hfr(url, verbosity = 0):
    """wrapper to choose appropriate netCDF opener."""
    try:
        t, lat, lon, z, u, v = open_ccc_oma_mat(url, verbosity)
    except ValueError: # the cencalcurrents netCDF has different labels
        t, lat, lon, z, u, v = open_hfrnet_thredds_ncss(url, verbosity)
    except NameError:
        t, lat, lon, z, u, v = open_ccc_gnome_nc(url, verbosity)
    except Exception as e:
        raise e
        raise Exception('can only open netCDF datasets from hfrnet or cencalcurrents, not ' + url + e)
    return t, lat, lon, z, u, v


def open_ccc_oma_mat(url, tidx = -1, verbosity = 1):
    """Grab data from an open-boundary modal analysis interpolation."""
    if verbosity > 1: print 'getting: ', url
    matfile, header = urlretrieve(url)
    try: # try reading as hdf5 first
        data = h5py.File(matfile)
    except IOError: 
        data = sp.io.loadmat(matfile)['TUV'][0,0] #TODO look at the other fields
#    except ValueError, e: raise e # sometimes unknown mat file type
    t = data['TimeStamp'][0,0] #XXX silly extra dimensions
    lat = data['LonLat'][:,1] #XXX silly extra dimensions
    lon = data['LonLat'][:,0] #XXX silly extra dimensions
    z = data['Depth'][0,0] #XXX silly extra dimensions
    if np.isnan(z): z = 0
    u = unravel_oma(lat, lon, data['U'].squeeze()) / 100.
    v = unravel_oma(lat, lon, data['V'].squeeze()) / 100.
    lat = np.unique(lat)
    lon = np.unique(lon) #add this for now for consistent usage for plotting... until I move it into the currents module
    return t, lat, lon, z, u, v


def open_hfrnet_thredds_ncss(url, tidx = -1, verbosity = 0):
    """Grab data from a NetCDF Subset Service for Grids."""
    if not url.startswith('http://hfrnet.ucsd.edu/thredds/ncss/grid/HFRNet'):
        raise ValueError('Method intended for hfrnet ncss data, not:', url)
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

def make_ccc_oma_url(ts, protocol='http', host='cencalcurrents.org', 
    root='DataRealTime', dtype='Oma', region='MNTY'):
    """Returns a string providing the URL for OMA surfac current data."""
    if type(ts) in (int, float): ts = datetime.fromutctimestamp(ts)
    year_month = ts.strftime('%Y_%m')
    fn = '{dtype}_{region}_{ts}.mat'
    matfile = fn.format(dtype = dtype.lower(), region = region, 
        ts = ts.strftime('%Y_%m_%d_%H%M'))
    return '/'.join((protocol+':/',host,root,dtype,region,year_month,matfile))
    


def make_hfrnet_url():
    raise NotImplementedError

def make_ccc_gnome_url():
    raise NotImplementedError
    


def draw_monterey_bay():
    m = oa.maps.MontereyBay(resolution = 'l')
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
    if outdir: 
        fn = os.path.join(outdir,title.replace(' ','_').replace(':','')+'.png')
        plt.savefig(fn, dpi=1200)
    else: plt.show()    

if __name__ == "__main__":
    
    url = make_ccc_oma_url(datetime(2012,10,01,00,00))
#    url = 'http://hfrnet.ucsd.edu/thredds/ncss/grid/HFRNet/USWC/6km/hourly/RTV?var=u,v&north=37&south=35&east=-121&west=-123&time_start=2012-10-01T00:00:00Z&time_end=2012-10-01T01:00:00Z&accept=application/x-netcdf'
#    url = 'http://cencalcurrents.org/DataRealTime/Gnome/MNTY/2012_09/GNOME_MNTY_2012_09_17_2300.nc'
    #TODO write class/methods to generate these in a flexible but robust way, put them in oceanidanalysis package
#    main(url, outdir='/tmp')
    main(url)

