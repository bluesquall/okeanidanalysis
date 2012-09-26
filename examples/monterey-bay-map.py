#!/usr/bin/env python
"""
`monterey-bay-map.py`
=====================

An example script to generate a map of the area around Monterey Bay.

"""
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap

import oceanidanalysis as oa
#TODO subclass basemap with default bounding box, projection, etc and include in oa.maps
bmres = ['l','i','h','f']

def main(verbose=0, resolution='l', r=None, g=None, outfile=None, 
        bluemarble=None, topography=None, bathymetry=None, 
        **kwargs):
    """Draw a map of Monterey Bay."""
    if verbose > 0: print 'Using Basemap to generate a map of Monterey Bay'    
    if r: resolution = bmres[r]
    m = oa.maps.MontereyBay(resolution=resolution, **kwargs)
    #TODO handle bluemarble, topography, etc.
#    m.drawcoastlines()
#    m.fillcontinents(color='coral',lake_color='aqua')
#    m.drawmapboundary(fill_color='aqua')
#    m.drawrivers(color='b')
    if g:
        m.drawparallels(np.arange(-89,89,0.1),labels=[1,1,0,0],fontsize=10)
        m.drawmeridians(np.arange(-180,180,0.1),labels=[0,0,1,1],fontsize=10)
    plt.suptitle("Monterey Bay ({} Projection)".format(m.projection))
        #TODO pretty print projection
    if outfile: plt.savefig(outfile) #TODO save args...
    else: plt.show()
    return m

if __name__ == "__main__":
    import argparse
    # instantiate parser
    parser = argparse.ArgumentParser(description='draw a map of Monterey Bay', 
        prefix_chars='-+')
    # add positional arguments
    # add optional arguments
    parser.add_argument('-V', '--version', action='version', 
        version='%(prog)s 0.0.1',
        help='display version information and exit')
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='display verbose output')
    parser.add_argument('+r', action='count', default=0,
        help='increase Basemap resolution')
        #TODO maximum?, accept string args as well?
    parser.add_argument('--resolution', default='l',
        help='set Basemap resolution')
    parser.add_argument('-p', '--projection', type=str, 
        default='tmerc',
        help='type of map projection to use')
    parser.add_argument('-o', '--outfile', metavar='filename', 
        type=argparse.FileType('wt'), help='output file')
    # add options with prefixes
    parser.add_argument('-g', action="store_false", default=None,
        help='do not include a grid')
    parser.add_argument('+g', action="store_true", default=None,
        help='include a grid')
    # mutually exclusive options...
    parser.add_argument('--bluemarble', action="store_false", default=None,
        help='do not use bluemarble image')
    parser.add_argument('++bluemarble', action="store_true", default=None,
        help='use bluemarble image')
    parser.add_argument('--topography', action="store_false", default=None,
        help='mask land')
    parser.add_argument('++topography', action="store_true", default=None,
        help='display topography')
    parser.add_argument('--bathymetry', action="store_false", default=None,
        help='mask ocean')
    parser.add_argument('++bathymetry', action="store_true", default=None,
        help='display bathymetry')
    # actually parse the arguments
    args = parser.parse_args()
    # call the main method to do something interesting
    main(**args.__dict__) #TODO more pythonic?
