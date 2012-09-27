"""
oceanidanalysis.maps
====================

Plotting tools and wrappers to generate common map views of MBARI LRAUV data.

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

## choose one of the methods below (or something similar) to make a map
#m = Basemap(llcrnrlon=-130,llcrnrlat=60,urcrnrlon=-120,urcrnrlat=70,
#            resolution='h',projection='tmerc',lon_0=-4,lat_0=0)
#m = Basemap(width=920000,height=1100000,
#            resolution='f',projection='tmerc',lon_0=-4.2,lat_0=54.6)

class Map(Basemap):
    """Subclass of basemap.Basemap with standard colors and boundaries.

    """

    def __init__(self, *args, **kwargs):
        dkw = self.get_init_defaults() # don't want to overwrite the defaults
        dkw.update(kwargs) # but do want to accept overrides
        Basemap(*args, **dkw)
#        super().__init__(**dkw) #TODO reasons to use this or not...
#        self.drawcoastlines(color = 'black')
#        self.fillcontinents(color='coral',lake_color='aqua')
#        self.drawrivers(color = 'blue')


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
    #TODO is there a more pythonic way of handling defaults for subclasses?
    def get_init_defaults(self):
        return dict(lat_0 = 36.75, lon_0 = -121.0,
            llcrnrlat = 36.5, llcrnrlon = -122.5,
            urcrnrlat = 37, urcrnrlon = -121.75,
            projection = 'tmerc', resolution = 'i')

#XXX should I even need to override the init argument this way?
#    def __init__(self, *args, **kwargs):
#        Map(*args, **kwargs)
#        super

    def draw_parallels(self, ):
        """Overloaded method with default args.

        """
        raise NotImplementedError


    def draw_meridians(self, ):
        """Overloaded method with default args.

        """
        raise NotImplementedError


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



