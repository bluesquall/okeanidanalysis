"""
okeanidanalysis.logs
====================

"""

import os
import datetime

import numpy as np
import scipy as sp
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt

import okeanidanalysis.lib as oalib


def logpath(file_name, vehicle_name=None, logset=None, 
        deployment=None, year=None, logtype='full', 
        log_root=os.path.join('/','mbari','LRAUV'), verbosity=1 ):
    """Return full path to an LRAUV log.

    Parameters
    ----------
    file_name : str
        The name of the unpacked log (e.g., 201405230522_201405231223.mat)
    vehicle_name: str [None]
        The name of the vehicle (e.g., Tethys)
    logset : str [None]
        The string identifying the actual set of logs (e.g., 20140523T052244)
    deployment : str [None]
        The identifier for the deployment (e.g., 20140522_20140528)
    logtype : str ['full'], 'SBD', '3G', 'HotSpot'

    log_root: str or path
        Path to the root directory containing the logs for all the vehicles.

    Returns
    -------
    log_path : str
        Full path to the log.

    """
    logtypes = { 'full': 'missionlogs', 'missionlogs': 'missionlogs', 
            'mission': 'missionlogs', 'shore': 'sbdlogs', 'sbd': 'sbdlogs', }

    if year is None: 
        year = int(file_name[:4]) 
        # TODO: catch exceptions, handle science_ prefixes

    if vehicle_name is not None:
        branch = [vehicle_name]
        try: 
            branch.append(logtypes[logtype])
            branch.append(str(year))
            if deployment is not None:
                branch.append(deployment)
                if logset is not None:
                    branch.append(logset)
        except KeyError: warnings.warn('Unknown log type' + logtype)
        # TODO: handle months in sbdlogs directory paths
        log_root = os.path.join(log_root, *branch)
    if verbosity > 0: print('search starting at: {0}'.format(log_root))
    
    for root, dirs, files in os.walk(log_root):
        if file_name in files:
            return os.path.join(root, file_name)
            

# TODO provide alternate access to netCDF files through OkeanidNetCDF?

class OkeanidLog(h5py.File):

    def __init__(self, name, mode='r', **kw):
        """Overloaded init method for h5py.File (read-only by default).

        """
        h5py.File.__init__(self, name, mode, **kw)


    def print_tree(self, root='/', verbosity=0): 
        for k0, i0 in self[root].items():
            if isinstance(i0, h5py.Dataset) and verbosity > 0:
                print ('found level 0 dataset {0}'.format(k0))
                # TODO collect the dataset size
            elif isinstance(i0, h5py.Group):
                print('found level 0 group {0}'.format(k0))
                # ... continue into the group -- there should be a smart war
                # to do this without rewriting a lot of code...
                for k1, i1 in i0.items():
                    if isinstance(i1, h5py.Dataset) and verbosity > 0:
                        print('\tfound level 1 dataset {0}'.format(k1))
                        # TODO collect the dataset size
                    elif isinstance(i1,h5py.Group):
                        print('\tfound subgroup {0}'.format(k1))
                        for k2, i2 in i1.items():
                            if isinstance(i2, h5py.Dataset) and verbosity>0:
                                print('\t\tfound level 2 dataset {0}'.format(k2))
                            elif isinstance(i2, h5py.Group):
                                print('\t\tfound subsubgroub'.format(k2))


    def grep_tree(self, pattern):
        raise NotImplementedError


    def cat(self, *a):
        for filename in a:
            f = OkeanidLog(filename,'r') # open another log read-only

            f.close()
        raise NotImplementedError
        # TODO  This method would be very useful for making a single log
        #       for each deployment.


    def units(self, x):
        """Stop-gap method to decode funky units records in HDF5/.mat

        """
        u = ''.join([chr(d) for d in self[x]['units'][:]])
        if (u in ['n/a']) and (x in ['latitude', 'longitude']):
            u = 'radian' # assume radians
        return u


    def timeseries(self, x, return_epoch=False, return_list=False, 
            convert=None, timeslice=None, rmnans=False, **kw):
        """Extract simple timeseries.
        
        e.g.,   depth, t = slate.timeseries('depth')
                depthCmd, t = slate.timeseries('VerticalControl/depthCmd')
                etc.

        """
        # TODO it seems like the replace statement below is not getting evaluated
        try: v = self[x.replace('.','/')]['value'][:].squeeze()
        except Exception:
            print('could not read value for {0}'.format(x))
#            raise e
        if convert: 
            v = convert(v)
        t = oalib.matlab_datenum_to_python_datetime(self[x]['time'][:].squeeze())
        if return_epoch: # XXX does this if really slow things down?
            t = oalib.python_datetime_to_unix_epoch(t)
        t = np.array(t)
        if timeslice:
            v = v[np.logical_and(t > timeslice[0], t < timeslice[1])]
            t = t[np.logical_and(t > timeslice[0], t < timeslice[1])]
        if rmnans:
            v, t = oalib.rmnans(v, t)
        if return_list:
            v, t = v.tolist(), t.tolist()
        return v, t


    def plot_timeseries(self, x, *a, **kw):
        """A convenience function for plotting time-series."""
        kw.update(return_epoch=False)
        v, t = self.timeseries(x, **kw)
        for k in ('return_epoch', 'convert', 'timeslice', 'rmnans'): 
            trash = kw.pop(k, None)
        if not a: a = '-' # plot a line by default
        if 'label' not in kw: 
            kw.update({'label': x.replace('platform ','').replace('_',' ')})
        if 'axes' in kw: # deal with possible bug in plot_date?
            ax = kw.pop('axes')
            ax.plot_date(t, v, *a, **kw)
            ax.set_xlim(ax.xaxis.get_data_interval()) # update time limits
        else: # just make a new axis
            plt.plot_date(t, v, *a, **kw)
            ax = plt.gca()
        plt.gcf().autofmt_xdate()
        return ax


    def interpolate_timeseries(self, x, t, **kw):
        """Convenience wrapper for sp.interpolate.interp1d

        note: can alternately implement interpolation using:                      
            sp.interpolate.UnivariateSpline                                 
            with a small (e.g., 1e-6) smoothing factor...                       
 
        """
        if type(t[0]) is datetime.datetime: t = oalib.python_datetime_to_unix_epoch(t)
        elif type(t[0]) is not float: print('time argument must be datetime or float epoch seconds') # TODO exception
        v, t_v = self.timeseries(x, rmnans=True, return_epoch=True) # r_e faster??
        interpolant = sp.interpolate.interp1d(t_v, v, **kw)
        try: # assume time array is Unix epoch float seconds
            return interpolant(t)
        except ValueError: # A value in x_new is below the interpolation range.
            kw.update(dict(bounds_error=False))
            interpolant = sp.interpolate.interp1d(t_v, v, **kw)
            return interpolant(t)
            # TODO clean up


    def interpolate_trajectory(self, t, return_degrees=True, **kw):
        lat = self.interpolate_timeseries('latitude', t, **kw)
        lon = self.interpolate_timeseries('longitude', t, **kw)
        dep = self.interpolate_timeseries('depth', t, **kw)
        if return_degrees and self.units('latitude') is 'radian':
            lat, lon = np.rad2deg(lat), np.rad2deg(lon)
        return lon, lat, dep


    def map_track(self, mapobject, component=None, *a, **kw):
        """Draw the track (latitude, longitude) on a basemap object.

        Parameters
        ----------
        mapobject : a map generated by `basemap`
        component: str [None]
            The component name to plot latitude and longitude from  (e.g., DeadReckonUsingMultipleVelocitySources)


        Keywords
        --------        
        start_stop_marker : bool [False]
            Flag controlling whether to plot markers at the start end end.
        timeslice : TODO

        Returns
        -------
        log_path : str
            Full path to the log.

        """
        if component is None or component.lower() == 'universal':
            latvar = 'latitude'
            lonvar = 'longitude'
        elif component.lower() == 'fix':
            latvar = 'latitude_fix'
            lonvar = 'longitude_fix'
        else:
            latvar = '/'.join((component,'latitude'))
            lonvar = '/'.join((component,'longitude'))
        start_stop_marker = kw.pop('start_stop_marker', False)
        try:
            timeslice = kw.pop('timeslice')
            lats, t = self.timeseries(latvar, timeslice=timeslice)
            lons, t = self.timeseries(lonvar, timeslice=timeslice)
        except KeyError:
            lats = self['/'.join((latvar,'value'))][:]
            lons = self['/'.join((lonvar,'value'))][:]
        if self.units(latvar) is 'radian':
            lats, lons = np.rad2deg(lats), np.rad2deg(lons)
        mapobject.draw_track(lats, lons, *a, **kw)
        if start_stop_marker is True: # TODO: accept input marker shapes
            mapobject.plot(lons[0], lats[0], 'go', latlon=True)
            mapobject.plot(lons[-1], lats[-1], 'r8', latlon=True)


    def meters_trajectory(self, projection):
        """
        
        Monterey Bay in UTM:
            projection = pyproj.Proj(proj='utm', zone=10, ellps='WGS84')

        """
        g = np.hstack((self['longitude/value'][:],self['latitude/value'][:]))
        lat = self['latitude/value'][:]
        lon = self['longitude/value'][:]
        dep = self['depth/value'][:]
        junk, lat, lon, dep = oalib.rmnans(lat + lon, lat, lon, dep)
#        if self.units('latitude') is 'radian':
#            lats, lons = np.rad2deg(lats), np.rad2deg(lons)
        if self.units('latitude') is 'radian': radflag = True
        else: radflag = False
        easting, northing = projection(lon, lat, radians=radflag)
        return np.vstack((northing, easting, dep))
# TODO include an interpolation for trajectory in meters as well


    def map_meters_trajectory(self, projection, origin=None, **kw):
        """

        """
        n, e, d = self.meters_trajectory(projection)
        if origin in ['mean', 'average']:
            e0, n0 = e.mean(), n.mean()
        elif origin is not None:
            o0, o1, o_unit = origin
            if o_unit in ['degree', 'deg', 'degrees']: 
                e0, n0 = projection(o1, o0)
            elif o_unit in ['meter', 'm', 'meters']:
                e0, n0 = o0, o1
            else:
                raise NotImplementedError('{0} not supported'.format(o_unit))
        else:
            e0, n0 = 0, 0
        plt.plot(e - e0, n - n0, **kw) # plot should take care of axis...
        return plt.gca(), e0, n0


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
        #figsize = (figwidth, figwidth/oalib.golden_ratio)
        figsize = (9, 6.5) # good for letter paper
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
        # TODO do this again now that middle labels are removed

        self.plot_timeseries('depth', '-', axes=depth_ax)
        self.plot_timeseries('platform_pitch_angle', axes=pitch_ax)
        self.plot_timeseries('platform_mass_position', axes=mass_ax)
        self.plot_timeseries('platform_buoyancy_position', axes=buoyancy_ax)
        self.plot_timeseries('platform_elevator_angle', axes=control_surface_ax)
        # TODO  Include another panel with VerticalControl mode (iff present)

        # TODO only if engineering data is requested...
        ### add to depth axes ###
        depth_science = {
                'Depth_Keller/depth': 'c-',
                'CTD_NeilBrown/depth': 'k-',
                'Depth_MSI_US300/depth': 'm-'}
        for k, v in depth_science.items():
            try: self.plot_timeseries(k, v, axes=depth_ax)
            except: print('no {0}'.format(k))

        depth_engineering = {
                'VerticalControl/smoothDepthInternal': 'r-',
                'VerticalControl/depthCmd': 'g-',
                'VerticalControl/depthErrorInternal': 'g:'}
        for k, v in depth_engineering.items():
            try: self.plot_timeseries(k, v, axes=depth_ax)
            except: print('no {0}'.format(k))
        # TODO only if sw debug flag is set 
        depth_rate_engineering = {
                'VerticalControl/depthRateCmd': 'gray',
                'VerticalControl/depth_rate': 'gray', # XXX why same color?
                }
        for k, v in depth_rate_engineering.items():
            try: 
                self.plot_timeseries(k, vi, axes=depth_ax, 
                        convert=oalib.make_multiplier(100))
            except: print('no {0}'.format(k))
        ### add to pitch axes ###
        pitch_engineering = {
                'AHRS_sp3003D/platform_pitch_angle': 'k-', 
                'DVL_micro/platform_pitch_angle': 'm-',
                'AHRS_3DMGX3/platform_pitch_angle': 'c-',
                'InternalSim/platform_pitch_angle': ':r',
                }
        for k, v in pitch_engineering.items():
            try: self.plot_timeseries(k, v, axes=pitch_ax)
            except: print('no {0}'.format(k))
        ### add to mass axes ###
        mass_engineering = {
                'VerticalControl/massPositionAction': 'g-', 
                'VerticalControl/massIntegralInternal': 'c-',
                'MassServo/platform_mass_position': 'r-',
                #'VerticalControl/massPitchErrorInternal': ':r',
                }
        for k, v in mass_engineering.items():
            try: self.plot_timeseries(k, v, axes=mass_ax)
            except: print('no {0}'.format(k))
        ### add to buoyancy axes ###
        buoyancy_engineering = {
                'VerticalControl/buoyancyAction': 'm-',
                'BuoyancyServo/platform_buoyancy_position': 'b-',
                }
        for k, v in buoyancy_engineering.items():
            try: 
                self.plot_timeseries(k, v,
#                        convert=oalib.make_multiplier(-10), 
                        axes=buoyancy_ax)
            except: print('no {0}'.format(k))
        ### add to control surface axes ###
        control_surface_engineering = {
                'VerticalControl/elevatorAngleAction': 'm-', 
                'VerticalControl/elevatorIntegralInternal': 'm:',
                'ElevatorServo/platform_elevator_angle': 'c-',
                }
        for k, v in control_surface_engineering.items():
            try: 
                self.plot_timeseries(k, v, convert = np.rad2deg, 
                   axes=control_surface_ax)
            except: print('no {0}'.format(k))
 

        # TODO only if supporting data is requested
        ### add other supporting data ###
        try: self.plot_timeseries('CTD_NeilBrown/depth', 'k-', axes=depth_ax)
        except: print('no CTD_NeilBrown/depth')
        try: self.plot_timeseries('Depth_MSI_US300', 'm-', axes=depth_ax)
        except: print('no Depth_MSI_US300')


        ### print additional information ###
        buoyancyNeutral = ('Config/Control/buoyancyNeutral',
                'Config/Servo/buoyancyNeutral')
        for s in buoyancyNeutral:
            try:
                print('{0} = {1} {2}'.format(s, self[s+'/value'], self[s+'/units']))
            except:
                print('{0} not found'.format(s))
        
#       VertMd(0=N/A,1=Surf,2=Dep,3=DepRt,4=Pit0,5=Pit,6=PitRt,7=M&E,8=Flt),
#       VertHoldMd(0=N/A,1=Ms,2=El,3=Both)
        try:
            v, t = self.timeseries('VerticalControl/verticalMode')
            oalib.plot_date_blocks(t, v, axes=control_mode_ax, colormap=mpl.cm.jet)
        except: print('VerticalControl/verticalMode not found')

        depth_ax.invert_yaxis()
        for ax in fig.get_axes():
            ax.grid(True)
            try:
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                        fontsize='small')
            except:
                print('uncaught exception for legend...')
        for ax in fig.get_axes()[:-1]:
            plt.setp(ax.get_xticklabels(), visible=False)

        depth_ax.set_title(os.path.basename(self.filename))
        control_mode_ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%H:%M'))
        plt.setp(control_mode_ax.get_xticklabels(), rotation=30,
                fontsize='small')

# TODO decide whether I really want the extra classes below
#class VehicleLog(OkeanidLog):
#class ShoreLog(OkeanidLog):
#class ShipLog(OkeanidLog):
