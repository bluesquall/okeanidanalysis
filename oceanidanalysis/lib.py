"""
oceanidanalysis.lib
===================

Generally useful methods that span across submodules.

"""

import numpy as np
import scipy as sp
import scipy.interpolate

def injectlocals(l, skip=['self','args','kwargs'], **kwargs):
    """Update a dictionary with another, skipping specified keys."""
    if l.has_key('kwargs') : kwargs.update(l['kwargs'])
    kwargs.update(dict((k, v) for k, v in l.items() if k not in skip))
    return kwargs

def gridravel(ix, iy, iz, rmnan=True, returnxy=True):
    """Reduce a grid to three vectors."""
    if ix.squeeze().ndim == 1: ix, iy = np.meshgrid(ix, iy)
    if not rmnan: 
        if returnxy: return ix.ravel(), iy.ravel(), iz.ravel()
        else: return iz.ravel()
    else:
        nans = np.isnan(iz.ravel()) # use ravel for a view since it's faster
        ox = ix.ravel()[~nans]
        oy = iy.ravel()[~nans]
        oz = iz.ravel()[~nans]
        if returnxy: return ox, oy, oz
        else: return oz

def gridunravel(ix, iy, iz, returnxy=False, ):
#    x = np.unique(ix)
#    y = np.unique(iy)
#TODO ensure monotonicity...
    gx, gy = np.meshgrid(np.unique(ix), np.unique(iy))
    #TODO alternate implementation without griddata
    gz = sp.interpolate.griddata((ix, iy), iz, (gx,gy), method='nearest')
    #TODO using griddata for this is overkill, and may not be sustainable in the future -- write a more specific replacement that will handle missing values as masked _or_ nan, probably using np.ravel_multi_index
    if returnxy: return gx, gy, gz
    else: return gz
