"""
oceanidanalysis.maps
====================

Plotting tools and wrappers to generate common map views of MBARI LRAUV data.

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from oceanidanalysis import lib

## choose one of the methods below (or something similar) to make a map
#m = Basemap(llcrnrlon=-130,llcrnrlat=60,urcrnrlon=-120,urcrnrlat=70,
#            resolution='h',projection='tmerc',lon_0=-4,lat_0=0)
#m = Basemap(width=920000,height=1100000,
#            resolution='f',projection='tmerc',lon_0=-4.2,lat_0=54.6)

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
        labels=[1,1,0,0], fontsize=10, **kwargs):
        """Overloaded method with default args.

        """
        kwargs.update(dict(labels=labels, fontsize=fontsize)) #TODO pythonic
        if circles is None: circles = self.arangelat(dlat)
        Basemap.drawparallels(self, circles, **kwargs)


    def drawmeridians(self, circles=None, dlon=1.,
        labels=[0,0,1,1], fontsize=10, **kwargs):
        """Overloaded method with default args.

        """
        kwargs.update(dict(labels=labels, fontsize=fontsize)) #TODO pythonic
        if circles is None: circles = self.arangelon(dlon)
        Basemap.drawmeridians(self, circles, **kwargs)


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

    def draw_currents(self, current, depth=0, **kwargs):
        """Quiver plot the ocean current.
        
        """
        ur, vr, xp, yp = self.rotate_vector(u, v, lon, lat, returnxy = True)
        q = self.quiver(xp, yp, ur, vr, **kwargs) 
            #or specify, e.g., width=0.003, scale=400)
        qkey = plt.quiverkey(q, 0.95, 1.05, 25, '25 m/s', labelpos='W') 
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
        ur, vr, xp, yp = m.transform_vector(u,v,lons,lats,nxv,nyv,returnxy=True)
        self.barbs(xp, yp, ur, vr, **default) #TODO what does this return?
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


    def draw_mars(self, *args, **kwargs):
        """Mark position of MARS cabled observatory.

        """
        default = dict(color = 'red', marker = 'square', label = 'MARS')
        default.update(kwargs)
        mars_lat = 0 #TODO
        mars_lon = 0 #TODO
        mars_depth = 0 #TODO
        x, y = self(mars_lon, mars_lat) # position in projection
        # self.plot(x, y, **default) #TODO what figure does it go to by default?
        raise NotImplementedError



