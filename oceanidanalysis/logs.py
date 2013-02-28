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

    def print_tree(self,):
        for k0, i0 in self.items():
            if isinstance(i0, h5py.Dataset):
                print 'found level 0 dataset', k0
                # TODO collect the dataset size
            elif isinstance(i0, h5py.Group):
                print 'found level 0 group', k0
                # ... continue into the group -- there should be a smart war
                # to do this without rewriting a lot of code...
                for k1, i1 in i0.items():
                    if isinstance(i1, h5py.Dataset):
                        print '\tfound level 1 dataset', k1
                        # TODO collect the dataset size
                    elif isinstance(i1,h5py.Group):
                        print '\tfound subgroup', k1
                        for k2, i2 in i1.items():
                            if isinstance(i2, h5py.Dataset):
                                print '\t\tfound level 2 dataset', k2
                            elif isinstance(i2, h5py.Group):
                                print '\t\tfound subsubgroub', k2
#                            else: print 'found unknown', k2
#                        else: print 'found unknown', k1
#                    else: print 'found unknown', k0


    def cat(self, *a):
        for filename in a:
            f = OceanidLog(filename,'r') # open another log read-only

            f.close()
        raise NotImplementedError
        # TODO  This method would be very useful for making a single log
        #       for each deployment.


    def plot_timeseries(self, x, *a, **kw):
        "A convenience function for plotting time-series."""
        plt.plot_date(self[x]['time'][:], self[x]['value'][:], *a, **kw)
        # TODO  let it accept ax as an optional argument


    def map_trajectory(self, mapobject, *a, **kw):
        lats = np.rad2deg(self['latitude']['value'][:])
        lons = np.rad2deg(self['longitude']['value'][:])
        x, y = mapobject(lons, lats)
        mapobject.plot(x, y, *a, **kw)


    def meters_trajectory(self, projection):
        """
        
        Monterey Bay in UTM:
            projection = pyproj.Proj(proj='utm', zone=10, ellps='WGS84')

        """
        latitude = np.rad2deg(self['latitude']['value'][:])
        longitude = np.rad2deg(self['longitude']['value'][:])
        depth = self['depth']['value'][:]
        northing, easting = projection(longitude, latitude)
        return np.vstack((northing, easting, depth)).T


# TODO move trajectory (time) interpolation tool into this module
# TODO include an interpolation for trajectory in meters as well

# TODO decide whether I really want the extra classes below
#class VehicleLog(OceanidLog):
#class ShoreLog(OceanidLog):
#class ShipLog(OceanidLog):
