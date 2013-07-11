"""
okeanidanalysis.maps
====================

Plotting tools and wrappers to generate common map views of MBARI LRAUV data.

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from okeanidanalysis import lib

class Map(Basemap):
    """Subclass of basemap.Basemap with standard colors and boundaries.

    """
    def arangelat(self, dlat=1.):
        try: 
            parallels = np.arange(self.llcrnrlat, self.urcrnrlat, dlat)
        except Exception, e: 
            # corner attributes dne, probably initialized some other way...
            raise e;
        return parallels
 

    def arangelon(self, dlon=1.):
        try: 
            meridians = np.arange(self.llcrnrlon, self.urcrnrlon, dlon)
        except Exception, e: 
            # corner attributes dne, probably initialized some other way...
            raise e;
        return meridians
        
       
    def drawparallels(self, circles=None, dlat=1., 
        labels=[1,0,0,0], fontsize=10, **kwargs):
        """Overloaded method with default args.

        """
        kwargs.update(dict(labels=labels, fontsize=fontsize)) #TODO pythonic
        if circles is None: circles = self.arangelat(dlat)
        Basemap.drawparallels(self, circles, **kwargs)


    def drawmeridians(self, circles=None, dlon=1.,
        labels=[0,0,0,1], fontsize=10, **kwargs):
        """Overloaded method with default args.

        """
        kwargs.update(dict(labels=labels, fontsize=fontsize)) #TODO pythonic
        if circles is None: circles = self.arangelon(dlon)
        Basemap.drawmeridians(self, circles, **kwargs)

    
    def drawgrid(self, lats=None, lons=None, 
            color='0.5', linewidth=0.5, dashes=[1, 0], **kwargs):
        """Draw a grid of latitude and longitude lines."""
        kwargs.update(dict(color=color, linewidth=linewidth, dashes=dashes))
        self.drawparallels(circles=lats, **kwargs)
        self.drawmeridians(circles=lons, **kwargs)


    def drawdefault(self):
        #TODO accept several kw dicts
        self.drawcoastlines()
        self.fillcontinents(color='coral',lake_color='aqua')
        #self.drawmapboundary(fill_color='aqua')
        self.drawmapboundary()
        self.drawrivers(color='b')


    def draw_bathymetry(self, isobaths):
        """Draw isobaths under water.

        """
        raise NotImplementedError


    def fill_bathymetry(self, cmap):
        """Fill bathymetry under water. (Color plot of sounding depths)

        """
        raise NotImplementedError

    def draw_topography(self, ):
        raise NotImplementedError

    def fill_topography(self, ):
        raise NotImplementedError

    def draw_buoys(self, ):
        """Permanent marker buoys.

        """
        raise NotImplementedError


    def draw_shipping_lanes(self, ):
        """Pretty Self-explanatory.

        """
        raise NotImplementedError


    def draw_track(self, track, **kwargs):
        """Draw a position track on the map (e.g., from Tethys or Daphne).

        """
        raise NotImplementedError
#TODO a track that changes color based on an ancillary variable

    def draw_currents(self, lat, lon, u, v, contourf_magnitude=True, **kwargs):
        """Quiver plot the ocean current.
        
        """
        if lat.ndim is 2: lat = np.sort(np.unique(lat))
        if lon.ndim is 2: lon = np.sort(np.unique(lon))
        um, vm, xm, ym = self.transform_vector(u, v, lon, lat, 
            len(lon), len(lat), returnxy = True, masked = True, order = 1)
        #TODO   pass kwargs to transform_vector?
        #TODO   optional input/output of *m variables above...
        if contourf_magnitude: 
            mm = (um**2 + vm**2)**0.5 # 2D current magnitude
            dc = 0.01
#TODO            cmax = max(mm) + dc 
            cmax = 0.5 + dc
            mmlevels = np.arange(0, cmax, dc) 
            self.contourf(xm, ym, mm, mmlevels, cmap=plt.cm.Blues)
            self.colorbar() #TODO pass kwargs
        q = self.quiver(xm, ym, um, vm, **kwargs) 
            #or specify, e.g., width=0.003, scale=400)
        qkey = plt.quiverkey(q, 0.1, -0.2, 1, '1 m/s', labelpos='W') 
            #TODO as defaults
        return q, qkey


    def draw_wind(self, wind, altitude, **kwargs):
        """Quiver plot the winds.

        (with or without a mask over the land)
        """
        #TODO redefine args, or unpack wind into u,v,lat,lon
        # transform from spherical to map projection coordinates (rotation
        # and interpolation).
        default = dict(length = 6, linewidth = 0.5,
            barbcolor = 'black', flagcolor = 'cyan', )
        nxv = 25; nyv = 25 #TODO can these be included in defaults?
        default.update(kwargs)
        um, vm, xm, ym = self.transform_vector(u,v,lons,lats,nxv,nyv,returnxy=True)
        self.barbs(xm, ym, um, vm, **default) #TODO what does this return?
        raise NotImplementedError


    def play(self, **kwargs):
        """Generate a movie using inputs with a time dimension.

        """
        raise NotImplementedError



class MontereyBay(Map):
    """A standard map canvas of Monterey Bay.

    """
    def __init__(self, lat_0 = 36.75, lon_0 = -121.0,
        llcrnrlat = 36.5, llcrnrlon = -122.5,
        urcrnrlat = 37, urcrnrlon = -121.75,
        projection = 'tmerc', resolution = 'i', **kwargs):
        """Overloaded method with default args.
        
        """
        Map.__init__(self, **lib.injectlocals(locals()))
        #TODO some handling if the map is defined in alternate fashion, e.g.:
#m = Basemap(width=920000,height=1100000,
#            resolution='f',projection='tmerc',lon_0=-4.2,lat_0=54.6)


    def drawparallels(self, dlat=.1, **kwargs):
        """Overloaded method with default args.

        """
        Map.drawparallels(self, dlat=dlat, **kwargs)


    def drawmeridians(self, dlon=.1, **kwargs):
        """Overloaded method with default args.

        """
        Map.drawmeridians(self, dlon=dlon, **kwargs)


    def draw_mbari(self, ):
        """Mark location of MBARI on the shore.

        """
        raise NotImplementedError


    def draw_canyon(self, ):
        """Draw boundaries of Monterey Canyon on the map.

        """
        raise NotImplementedError
#TODO other canyons, too?

    def draw_mountains(self, ):
        raise NotImplementedError


    def draw_mars(self,color='red', marker='s', label='MARS', **kwargs):
        """Mark position of MARS cabled observatory.

        """
        plot_kwargs = lib.injectlocals(locals())
        mars_lat = 36 + 42.7481/60 #TODO use proj or write a utility for oa.lib
        mars_lon =  -(122 + 11.2139/60)
        mars_depth = 891 # meters
        x, y = self(mars_lon, mars_lat) # position in projection
        self.plot(x, y, **plot_kwargs) 
        #TODO what figure does it go to by default?
        

