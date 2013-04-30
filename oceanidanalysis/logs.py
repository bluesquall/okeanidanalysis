"""
oceanidanalysis.logs
====================

Generally useful methods that span across submodules.

"""

# import cgi # do I actually need this anywhere?
import datetime, itertools

import numpy as np
import scipy as sp
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt

import gviz_api

import oceanidanalysis.lib as oalib

# TODO provide alternate access to netCDF files through OceanidNetCDF?

class OceanidLog(h5py.File):

    def print_tree(self, root='/', verbosity=0): 
        for k0, i0 in self[root].items():
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

    def grep_tree(self, pattern):
        raise NotImplementedError


    def cat(self, *a):
        for filename in a:
            f = OceanidLog(filename,'r') # open another log read-only

            f.close()
        raise NotImplementedError
        # TODO  This method would be very useful for making a single log
        #       for each deployment.


    def timeseries(self, x, return_epoch=False, return_list=False, 
            convert=None, **kw):
        """Extract simple timeseries.
        
        e.g.,   depth, t = slate.timeseries('depth')
                depthCmd, t = slate.timeseries('VerticalControl/depthCmd')
                etc.

        """
        v = self[x.replace('.','/')]['value'][:].ravel()
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
        trash = kw.pop('convert', None)
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


    def interpolate_trajectory(self, t, **kw):
        """
        
        note: can alternately implement interpolation using:                      
            sp.interpolate.UnivariateSpline                                 
            with a small (e.g., 1e-6) smoothing factor...                       
        """
        if type(t[0]) is datetime.datetime: tskw = dict(return_epoch=False)
        elif type(t[0]) in (float, np.float64): 
            tskw = dict(return_epoch=True)
        else: 
            print type(t[0])
            raise TypeError
        lat, t_lat = self.timeseries('latitude', **tskw)
        ilat = sp.interpolate.interp1d(t_lat, lat, **kw)
        lon, t_lon = self.timeseries('longitude', **tskw)
        ilon = sp.interpolate.interp1d(t_lon, lon, **kw)
        dep, t_dep = self.timeseries('depth', **tskw)
        idep = sp.interpolate.interp1d(t_dep, dep, **kw)
        return ilon(t), ilat(t), idep(t)       


    def map_trajectory(self, mapobject, *a, **kw):
        lats = self['latitude/value'][:]
        lons = self['longitude/value'][:]
#        print self['latitude/units'][:].ravel().tolist()
#        print self['longitude/units'][:].ravel().tolist()
        if self['latitude/units'][:].ravel().tolist() == [110, 47, 97]:
            #'radians': # TODO troubleshoot
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

    def comparison_timeseries(self, x, y, *a, **kw):
        #TODO add optional transformations for data in each channel
        x, tx = self.timeseries(x, return_epoch=True)
        y, ty = self.timeseries(y, return_epoch=True)
        t = np.hstack((tx,ty))
        t.sort() # in-place sort
        ix = np.interp(t,tx,x)
        iy = np.interp(t,ty,y)
        return t, ix, iy

 
    def plot_difference_timeseries(self, x, y, *a, **kw):
        t, ix, iy = self.comparison_timeseries(x, y)
        t = np.array([datetime.datetime.utcfromtimestamp(e) for e in t])
        print t.shape, ix.shape, iy.shape
        if 'axes' in kw: # deal with possible bug in plot_date?
            ax = kw.pop('axes')
            ax.plot_date(t, ix - iy, *a, **kw)
            return ax
        else: # just make a new axis
            plt.plot_date(t, ix - iy, *a, **kw)
            return plt.gca()


    def crossplot(self, x, y, correlation=False, *a, **kw):
        t, ix, iy = self.comparison_timeseries(x, y)
        s = plt.scatter(ix, iy, *a, **kw) # axes, etc pass through
        if correlation:
            raise NotImplementedError
            # TODO calculate linear correlation, add line to plot
            return s, ix, iy, cxy
        else: return s, ix, iy


    def vplane(self, ):
        """Plot control variables in vertical plane for review.

        Originally patterned after vplaneLR.m, by Rob McEwen.

        TODO: go back and insert any useful functionality that is commented
        out in vplane.m

        """
        #TODO more general multi-axis layout...
        figwidth = 13 # in inches...
        figsize = (figwidth, figwidth/oalib.golden_ratio)
        fig = plt.figure(figsize=figsize,)
        axkw = dict(frameon = True)
        left, width = 0.075, 0.6
        bh = 0.11
        pad = 0.04
        depth_ax = fig.add_axes((left, 6*pad+4.5*bh, width, bh*2), **axkw)
        axkw.update(dict(sharex = depth_ax))
        pitch_ax = fig.add_axes((left, 5*pad+3.5*bh, width, bh), **axkw)
        buoyancy_ax = fig.add_axes((left, 4*pad+2.5*bh, width, bh), **axkw)
        mass_ax = fig.add_axes((left, 3*pad + 1.5*bh, width, bh), **axkw)
        control_surface_ax = fig.add_axes((left, 2*pad + bh/2, width, bh), **axkw)
        control_mode_ax = fig.add_axes((left, pad, width, bh/2), **axkw)
        # TODO adjust scale and coverage for each axes
        axs = [depth_ax, pitch_ax, mass_ax, buoyancy_ax, 
                control_surface_ax, control_mode_ax] # list for convenience

        self.plot_timeseries('depth', '-', axes=depth_ax)
        self.plot_timeseries('platform_pitch_angle', convert=np.rad2deg, 
                axes=pitch_ax)
        self.plot_timeseries('platform_mass_position', axes=mass_ax)
        self.plot_timeseries('platform_buoyancy_position', axes=buoyancy_ax)
        self.plot_timeseries('platform_elevator_angle', axes=control_surface_ax)
        # TODO  Include another panel with VerticalControl mode (iff present)

        # TODO only if engineering data is requested...
        ### add to depth axes ###
        depth_engineering = {
                'VerticalControl/smoothDepthInternal': 'r-',
                'VerticalControl/depthCmd': 'g-',
                'VerticalControl/depthErrorInternal': 'g:'}
        for k, v in depth_engineering.iteritems():
            try: self.plot_timeseries(k, v, axes=depth_ax)
            except: print 'no', k
        # TODO only if sw debug flag is set 
        depth_rate_engineering = {
                'VerticalControl/depthRateCmd': 'gray',
                'VerticalControl/depth_rate': 'gray', # XXX why same color?
                }
        for k, v in depth_rate_engineering.iteritems():
            try: 
                self.plot_timeseries(k, vi, axes=depth_ax, 
                        convert=oalib.make_multiplier(100))
            except: print 'no', k
        ### add to pitch axes ###
        pitch_engineering = {
                'AHRS_sp3003D/platform_pitch_angle': 'k-', 
                'DVL_micro/platform_pitch_angle': 'm-',
                'AHRS_3DMGX3/platform_pitch_angle': 'c-',
                'InternalSim/platform_pitch_angle': ':r',
                }
        for k, v in pitch_engineering.iteritems():
            try: self.plot_timeseries(k, v, axes=pitch_ax)
            except: print 'no', k
        ### add to mass axes ###
        mass_engineering = {
                'VerticalControl/massPositionAction': 'g-', 
                'VerticalControl/massIntegralInternal': 'c-',
                'MassServo/platform_mass_position': 'r-',
                }
        for k, v in mass_engineering.iteritems():
            try: self.plot_timeseries(k, v, axes=mass_ax)
            except: print 'no', k
        ### add to buoyancy axes ###
        buoyancy_engineering = {
                'VerticalControl/buoyancyAction': 'm-',
                'BuoyancyServo/platform_buoyancy_position': 'b-',
                }
        for k, v in buoyancy_engineering.iteritems():
            try: 
                self.plot_timeseries(k, v,
                        convert=oalib.make_multiplier(-10), 
                        axes=buoyancy_ax)
            except: print 'no', k
        ### add to control surface axes ###
        control_surface_engineering = {
                'VerticalControl/elevatorAngleAction': 'm-', 
                'VerticalControl/elevatorIntegralInternal': 'm:',
                'ElevatorServo/platform_elevator_angle': 'b-',
                ' VerticalControl/massPitchErrorInternal': ':r',
                }
        for k, v in control_surface_engineering.iteritems():
            try: 
                self.plot_timeseries(k, v, convert = np.rad2deg, 
                   axes=control_surface_ax)
            except: print 'no', k
 

        # TODO only if supporting data is requested
        ### add other supporting data ###
        try: self.plot_timeseries('CTD_NeilBrown/depth', 'k-', axes=depth_ax)
        except: print 'no CTD_NeilBrown/depth'
        try: self.plot_timeseries('Depth_MSI_US300', 'm-', axes=depth_ax)
        except: print 'no Depth_MSI_US300'


        ### print additional information ###
        buoyancyNeutral = ('Config/Control/buoyancyNeutral',
                'Config/Servo/buoyancyNeutral')
        for s in buoyancyNeutral:
            try:
                print s, '=', self[s+'/value'], self[s+'/units']
            except:
                print s, 'not found'
        
#       VertMd(0=N/A,1=Surf,2=Dep,3=DepRt,4=Pit0,5=Pit,6=PitRt,7=M&E,8=Flt),
#       VertHoldMd(0=N/A,1=Ms,2=El,3=Both)
        try:
            v, t = self.timeseries('VerticalControl/verticalMode')
            oalib.plot_date_blocks(t, v, axes=control_mode_ax, colormap=mpl.cm.jet)
        except: 
            print 'VerticalControl/verticalMode', 'not found'

        depth_ax.invert_yaxis()
        for ax in axs:
            ax.grid(True)
            try:
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            except:
                print 'uncaught exception for legend...'

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
    
