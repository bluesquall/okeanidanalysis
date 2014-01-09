#!/usr/bin/env python
"""
`nav-tracks-in-monterey-bay.py`
===============================

An example script to generate a map of various possible navigation 
tracks in the area around Monterey Bay.

Can be run from command line, e.g.:

    python nav-tracks-in-monterey-bay.py /mbari/LRAUV/tethys/missionlogs/2013/20131219_20131220/20131219T204936/201312192049_201312202001.mat +rr

TODO: 
    * Add a NaN in when there is a gap larger than 1 minute, so that you can
      see breaks in plotted lines.

"""
import numpy as np
import matplotlib.pyplot as plt

import okeanidanalysis as oa
bmres = ['l','i','h','f']

def main(verbose=0, resolution='l', r=None, g=None, 
        infile=None, outfile=None, 
        bluemarble=None, topography=None, bathymetry=None, 
        **kwargs):
    """Draw a map of Monterey Bay."""
    if verbose > 0: print 'Using Basemap to generate a map of Monterey Bay'    
    if r: resolution = bmres[r]

    fig = plt.figure(figsize=(10,7.5))
    ax = fig.add_axes((0.05,0.05,0.9,0.9))
    m = oa.maps.MontereyBay(resolution=resolution, **kwargs)
    m.drawdefault()
    if g: m.drawgrid()

    slate = oa.logs.OkeanidLog(infile.name)
    slate.map_track(m, 'k-', label='Universal')
    
    timeslice = None
    # TODO: There is probably a more elegant & pythonic way to iterate 
    #       through the navigators and to define full linestyles, sizes,
    #       and other kwargs.
    navigatorlist = ['DeadReckonUsingMultipleVelocitySources',
            'DeadReckonWithRespectToSeafloor',
            'DeadReckonWithRespectToWater',
            'DeadReckonUsingDVLWaterTrack',
            'DeadReckonUsingCompactModelForecast',
            ]

    navigatorlinestyles = dict(universal='k',
            DeadReckonUsingCompactModelForecast='c:', 
            DeadReckonUsingDVLWaterTrack='b-',
            DeadReckonUsingMultipleVelocitySources='m-',
            DeadReckonWithRespectToSeafloor='g-',
            DeadReckonWithRespectToWater='c-')
    for n in navigatorlist:
        try:
            lats, t = slate.timeseries('/'.join([n, 'latitude']), timeslice=timeslice)
            lons, t = slate.timeseries('/'.join([n, 'longitude']), timeslice=timeslice)
            m.draw_track(lats, lons, navigatorlinestyles[n], label=n)
        except:
            print "could not find data for navigator:", n
    plt.legend(loc='lower left', fontsize='x-small')


    if outfile: plt.savefig(outfile) #TODO save args...
    else: plt.show()
    if verbose > 0: print 'm: ', m
    return m

if __name__ == "__main__":
    import argparse
    # instantiate parser
    parser = argparse.ArgumentParser(description='draw a map of Monterey Bay', 
        prefix_chars='-+')
    # add positional arguments
    parser.add_argument('infile', metavar='filename', 
        type=argparse.FileType('r'), help='input file (LRAUV .mat log)')
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
    parser.add_argument('-o', '--outfile', metavar='filename', 
        type=argparse.FileType('wt'), help='output file')
    # add options with prefixes
    parser.add_argument('-g', action="store_false", default=None,
        help='do not include a grid')
    parser.add_argument('+g', action="store_true", default=None,
        help='include a grid')
    # actually parse the arguments
    args = parser.parse_args()
    # call the main method to do something interesting
    m = main(**args.__dict__) #TODO more pythonic?
