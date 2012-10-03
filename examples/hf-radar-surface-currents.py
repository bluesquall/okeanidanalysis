#!/usr/bin/env python
"""
`hf-radar-surface-currents.py`
------------------------------

An example script to generate a surface current map of Monterey Bay.

"""
import os
from datetime import datetime
import matplotlib.pyplot as plt
import oceanidanalysis as oa

def draw_monterey_bay(resolution='l'):
    m = oa.maps.MontereyBay(resolution = resolution)
    m.drawcoastlines()
    m.drawdefault()
    m.drawgrid()
    return m 


def main(t, resolution='l', outfile=None, outdir=None):
    m = draw_monterey_bay(resolution)
    plt.hold(True)
    oma = oa.currents.OpenBoundaryModalAnalysis()
#TODO I'd like to be able to use a syntax like the one below, as well.
#    lat, lon, u, v = oma.open_datetime_url(datetime(2012,10,01,00,00))
#    m.draw_currents(lat, lon, u, v)
    oma.open_datetime_url(t)
    m.draw_currents(oma.latitude, oma.longitude, oma.u, oma.v)

    title = 'surface currents {}Z'.format(t.isoformat())
    plt.title(title)
    
    if outfile: plt.savefig(outfile) #TODO save args...
    if outdir: 
        fn = os.path.join(outdir,title.replace(' ','_').replace(':','')+'.png')
        plt.savefig(fn, dpi=1200)
    else: plt.show()    

if __name__ == "__main__":
    resolution = 'h'
    t = datetime(2012,10,01,00,00)
#    main(url, outdir='/tmp')
    main(t, resolution)

