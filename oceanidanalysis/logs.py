"""
oceanidanalysis.logs
====================

Generally useful methods that span across submodules.

"""

import numpy as np
import scipy as sp
import h5py
import matplotlib.pyplot as plt

# TODO provide alternate access to netCDF files through OceanidNetCDF?

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
        if not a: a = '-' # plot a line by default
        # TODO  How should I deal with deeply nested variables?
        if 'label' not in kw: 
            kw.update({'label': x.replace('platform','').replace('_',' ')})
        t, v = self[x]['time'][:], self[x]['value'][:]
        if 'convert' in kw: 
            f = kw.pop('convert')
            v = f(v)
        if 'tconvert' in kw: 
            f = kw.pop('tconvert')
            t = f(t)
        if 'axes' in kw: # deal with possible bug in plot_date?
            ax = kw.pop('axes')
            ax.plot_date(t, v, *a, **kw)
        else: # just make a new axis
            plt.plot_date(t, v, *a, **kw)


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

    def vplane(self, ):
        """Plot control variables in vertical plane for review.

        Originally patterned after vplaneLR.m, by Rob McEwen.

        """
        fig = plt.figure()
        axkw = dict(frameon = True)
        depth_ax = fig.add_subplot(5,1,1, **axkw)
        axkw.update(dict(sharex = depth_ax))
        pitch_ax = fig.add_subplot(5,1,2, **axkw)
        buoyancy_mass_ax = fig.add_subplot(5,1,3, **axkw)
        control_surface_ax = fig.add_subplot(5,1,4, **axkw)
#        control_mode_ax = fig.add_subplot(5,1,5, **axkw)
        # TODO adjust scale and coverage for each subplot
        axs = [depth_ax, pitch_ax, buoyancy_mass_ax, control_surface_ax, ]#control_mode_ax] # list for convenience

        self.plot_timeseries('depth', '-', axes=depth_ax)
        # TODO  Include other lines in this panel
#        depth_ax.set_ylim([1.1 * self['depth']['value'][:].max(), -1])

        self.plot_timeseries('platform_pitch_angle', axes=pitch_ax)
        # TODO  Include other lines in this panel

        self.plot_timeseries('platform_mass_position', axes=buoyancy_mass_ax)
        self.plot_timeseries('platform_buoyancy_position', 
                axes=buoyancy_mass_ax)
        # TODO  Include other lines in this panel
        
        self.plot_timeseries('platform_elevator_angle', 
                axes=control_surface_ax)
        # TODO  Include other lines in this panel

        # TODO  Include another panel with VerticalControl mode (iff present)
        
        depth_ax.invert_yaxis()
        for ax in axs:
            ax.grid(True)
            ax.legend()


# TODO decide whether I really want the extra classes below
#class VehicleLog(OceanidLog):
#class ShoreLog(OceanidLog):
#class ShipLog(OceanidLog):
