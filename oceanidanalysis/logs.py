"""
oceanidanalysis.logs
====================

Generally useful methods that span across submodules.

"""

# import cgi # do I actually need this anywhere?
import itertools

import numpy as np
import scipy as sp
import h5py
import matplotlib.pyplot as plt

import gviz_api

import oceanidanalysis.lib as oalib

# TODO provide alternate access to netCDF files through OceanidNetCDF?

class OceanidLog(h5py.File):

    def print_tree(self, verbosity=0): # keep this, it can be useful
        for k0, i0 in self.items():
            if isinstance(i0, h5py.Dataset) and verbosity > 0:
                print 'found level 0 dataset', k0
                # TODO collect the dataset size
            elif isinstance(i0, h5py.Group):
                print 'found level 0 group', k0
                # ... continue into the group -- there should be a smart war
                # to do this without rewriting a lot of code...
                for k1, i1 in i0.items():
                    if isinstance(i1, h5py.Dataset) and verbosity > 0:
                        print '\tfound level 1 dataset', k1
                        # TODO collect the dataset size
                    elif isinstance(i1,h5py.Group):
                        print '\tfound subgroup', k1
                        for k2, i2 in i1.items():
                            if isinstance(i2, h5py.Dataset) and verbosity>0:
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


    def timeseries(self, x, return_epoch=False, return_list=False, convert=None):
        """Extract simple timeseries.
        
        e.g.,   depth, t = slate.timeseries('depth')
                depthCmd, t = slate.timeseries('VerticalControl/depthCmd')
                etc.

        """
        v = self[x]['value'][:].ravel()
        if convert: 
            v = convert(v)
        t = oalib.matlab_datenum_to_python_datetime(self[x]['time'][:].ravel())
        if return_epoch: # XXX does this if really slow things down?
            t = oalib.python_datetime_to_unix_epoch(t)
        if return_list:
            return v.tolist(), t
        else: 
            return v, np.array(t)


    def plot_timeseries(self, x, *a, **kw):
        """A convenience function for plotting time-series."""
        v, t = self.timeseries(x, **kw)
        if not a: a = '-' # plot a line by default
        if 'label' not in kw: 
            kw.update({'label': x.replace('platform','').replace('_',' ')})
        if 'axes' in kw: # deal with possible bug in plot_date?
            ax = kw.pop('axes')
            ax.plot_date(t, v, *a, **kw)
            return ax
        else: # just make a new axis
            plt.plot_date(t, v, *a, **kw)
            return plt.gca()


    def map_trajectory(self, mapobject, *a, **kw):
        lats = self['latitude']['value'][:]
        lons = self['longitude']['value'][:]
        if self['latitude']['units'][:] is 'radians': # TODO troubleshoot
            lats, lons = np.rad2deg(lats), np.rad2deg(lons)
        x, y = mapobject(lons, lats)
        mapobject.plot(x, y, *a, **kw)


    def meters_trajectory(self, projection):
        """
        
        Monterey Bay in UTM:
            projection = pyproj.Proj(proj='utm', zone=10, ellps='WGS84')

        """
        latitude = np.rad2deg(self['latitude/value'][:])
        longitude = np.rad2deg(self['longitude/value'][:])
        depth = self['depth/value'][:]
        northing, easting = projection(longitude, latitude)
        return np.vstack((northing, easting, depth)).T


# TODO move trajectory (time) interpolation tool into this module
# TODO include an interpolation for trajectory in meters as well


    def crossplot(self, x, y, correlation=False, *a, **kw):
        #TODO add optional transformations for data in each channel
        x, tx = self.timeseries(x, return_epoch=True)
        y, ty = self.timeseries(y, return_epoch=True)
        t = np.hstack((tx,ty))
        t.sort() # in-place sort
        ix = np.interp(t,tx,x)
        iy = np.interp(t,ty,y)
        s = plt.scatter(ix, iy, *a, **kw) # axes, etc pass through
        if correlation:
            raise NotImplementedError
            # TODO calculate linear correlation, add line to plot
            return s, ix, iy, cxy
        else: return s, ix, iy


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
        try: 
            self.plot_timeseries('VerticalControl/smoothDepthInternal', 
                    'r-', axes=depth_ax)
        except: print 'no VerticalControl/smoothDepthInternal'
        try:
            self.plot_timeseries('VerticalControl/depthCmd', 
                    'g-', axes=depth_ax)
        except: print 'no VerticalControl/depthCmd'
        try:
            self.plot_timeseries('VerticalControl/depthErrorInternal', 
                    'g:', axes=depth_ax)
        except: print 'no VerticalControl/depthErrorInternal'
        try:
            self.plot_timeseries('VerticalControl/depthRateCmd', 
                    convert=oalib.make_multiplier(100), 
                    color='gray', axes=depth_ax)
        except: print 'no VerticalControl/depthRateCmd'






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

class GVisLog(OceanidLog):
    """Provides extra methods to interface with Google Charts API.
    
    (Really just separated into its own class for taste.)
    
    """
    
    def timeseries_to_gviz_data_table(self, group, **kw):
        """Create a DataTable for the Google Charts API.

        """
        description = { 'group': ('number', group),
                        'time': ('datetime', 'time') }
        data = [{'group': float(v), 'time': t} for v,t 
                in itertools.izip(*self.timeseries(group, **kw))]
        table = gviz_api.DataTable(description)
        table.LoadData(data)
        return table
        

    def timeseries_to_json_response(self, form, group, *a, **kw):
        """Generate a full API-compliant response to serve timeseries data.

        Parameters
        ----------
        form : an instance of cgi.FieldStorage() using psl cgi
        
        group : string
            points to the timeseries of interest, e.g., sea_water_temperature

        Returns
        -------
        response : string
            contains the content header, separation, and google.visualization.Query.setResponse

        References
        ----------
        https://developers.google.com/chart/interactive/docs/dev/implementing_data_source#responseformat

        """
        tqxstr = form.getfirst('tqx')
        if not tqxstr:
            tqx = {} # empty dict, and probably bad request...
        else:
            tqx = dict([p.split(':') for p in tqxstr.split(';')])

        jsrkw = dict(columns_order=('time', 'group'), order_by='time',
# XXX not handled yet...                responseHandler='google.visualization.Query.setResponse',
                )

        if 'version' in tqx: 
            jsrkw.update(version=tqx['version'])
        if 'reqId' in tqx: 
            jsrkw.update(req_id=tqx['reqId'])
        # TODO handle status other than OK...
        # TODO handle sig... if sig in tqx: jsrkw.update(req_id=tqx['reqId'])
        if 'out' in tqx: 
            if tqx['out'] is not 'json': 
                raise NotImplementedError
        # TODO these are _supposed_ to be defined and handled...
        #if 'responseHandler' in tqx: 
        #    jsrkw.update(responseHandler=tqx['responseHandler'])
        #if 'outFileName' in tqx: 
        #    raise NotImplementedError
        table = self.timeseries_to_gviz_data_table(group, *a, **kw)
        return "Content-type: text/plain\n\n" + table.ToJSonResponse(**jsrkw)
    
