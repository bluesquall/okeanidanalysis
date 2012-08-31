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
#    def __init__(self, *args, **kwargs):
#        super foo bar choo (whatever)
        self.drawcoastlines(color = 'black')
        self.fillcontinents(color='coral',lake_color='aqua')
        self.drawrivers(color = 'blue')


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
        raise NotImplementedError


    def draw_wind(self, wind, altitude, **kwargs):
        """Quiver plot the winds.

        (with or without a mask over the land)
        """
        raise NotImplementedError


    def play(self, **kwargs):
        """Generate a movie using inputs with a time dimension.

        """
        raise NotImplementedError



class MontereyBay(Map):
    """A standard map canvas of Monterey Bay.

    """

    def __init__(self, *args **kwargs):
        bmkwargs = dict(
            llcrnrlat = 50, llcrnrlon = -130,
            urcrnrlat = 60, urcrnrlon = -120,
            resolution = 'h', 
            projection = 'tmerc', lat_0 = 55, lon_0 = -110,
            )
        bmkwargs.update(kwargs) # pass any keyword args through
        
#        super foo bar choo (whatever this needs to be)

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



    def draw_mars(self, ):
        """Mark position of MARS cabled observatory.

        """
        raise NotImplementedError



