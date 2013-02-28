#!/usr/bin/env python
"""
monterey-bay-gmtpy.py
=====================

A gmtpy example to map Monterey Bay.

"""

import gmtpy

def main(minlat=36.5, minlon=-122.5, maxlat=37.0, maxlon=-121.75):
    """Generate a map of Monterey Bay using `GMT` through `gmtpy`."""
    gmt = gmtpy.GMT(config={'BASEMAP_TYPE':'fancy', 'PLOT_DEGREE_FORMAT':'D'})
    gmt.pscoast( R='{0}/{1}/{2}/{3}'.format(minlon, maxlon, minlat, maxlat), 
                 J='M18', # projection
                 B='WSn0.1g0.05p', # border
                 D='f', # resolution (e.g., for coastlines)
                 S=(114,159,207), 
                 G=(233,185,110),
                 W='thinnest',
                 I='a/4p/blue', # all waterways ...
                 L='fx3/0.5/36.75/20+l')
    gmt.psriver
    return gmt


if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser(description='GMT a map of Monterey Bay')
    parser.add_argument('-V', '--version', action='version', 
        version='%(prog)s 0.0.1', help='display version information and exit')
    parser.add_argument('-o', '--outfile', metavar='filename', 
        default=os.path.join('/','tmp','monterey-bay.gmt.pdf'),
        type=argparse.FileType('w'), help='output file')
    args = parser.parse_args()    

    gmt = main()
    gmt.save(args.outfile.name)
