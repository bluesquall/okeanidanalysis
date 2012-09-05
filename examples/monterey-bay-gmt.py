#!/usr/bin/env python
"""
monterey-bay-gmt.py
===================

A gmtpy example to map monterey bay.

"""

import gmtpy

if __name__ == "__main__":
    import argparse
#TODO argparse command line...
    gmt = gmtpy.GMT( config={'BASEMAP_TYPE':'fancy', 'PLOT_DEGREE_FORMAT':'D'} )
    gmt.pscoast( 
                 R='-122.5/-121.75/36.5/37',
                 J='M18',
                 B='WSn0.1g0.05p',
                 D='f',
                 S=(114,159,207),
                 G=(233,185,110),
                 W='thinnest',
                 I='a/4p/blue', # all waterways ...
#                 I='1/3p/blue', #XXX cannot repeat kwargs, try a str instead
#                 I='2/1p/blue',
                 L='fx3/0.5/36.75/20+l',
               )
    gmt.psriver
    gmt.save('/tmp/monterey-bay.gmtpy.pdf')
    gmt.save('/tmp/monterey-bay.gmtpy.eps')
