"""
okeanidanalysis.lib
===================

Generally useful methods that span across submodules.

"""

import time, datetime, pytz
import numpy as np
import scipy as sp
import scipy.interpolate
import matplotlib as mpl
import matplotlib.patches

UNIX_EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)                         

golden_ratio = 1.61803398875

def utime(t, convention=None):
    """Convert time to mircoseconds since epoch.

    Expects time given as a datetime object.

    """
#    typet = type(t)
#    if typet is datetime.datetime: # t = t.timetuple()
#        return int(time.mktime(t.timetuple())*1e6 + t.microsecond)
#    else:
#        raise TypeError('time type {} not recognized'.format(typet))
#TODO something to handle matlab datenum convention easily
    return [ue * 1e6 for ue in python_datetime_to_unix_epoch(t)]


def python_datetime_to_unix_epoch(dto):
    if type(dto) not in (list, np.ndarray): dto = [dto] # TODO is there a more elegant way?
    try:                                                                        
        return [(dt - UNIX_EPOCH).total_seconds() for dt in dto]
    except TypeError: # can't subtract offset-naive and offset-aware datetimes
        dto = (pytz.UTC.localize(dt) for dt in dto)
        return [(dt - UNIX_EPOCH).total_seconds() for dt in dto]  


def matlab_datenum_to_python_datetime(dn):                                      
    day = (datetime.datetime.fromordinal(int(n)) for n in dn)
    frac = (datetime.timedelta(days=n%1) for n in dn)
    shift = datetime.timedelta(days = 366)                                       
    return [d.replace(tzinfo=pytz.UTC) + f - shift for d, f in zip(day, frac)]
# TODO: consider explicitly returning an array if the input was an array 


def injectlocals(l, skip=['self','args','kwargs'], **kwargs):
    """Update a dictionary with another, skipping specified keys."""
    if 'kwargs' in l: kwargs.update(l['kwargs'])
    kwargs.update(dict((k, v) for k, v in l.items() if k not in skip))
    return kwargs


def make_multiplier(n): return lambda x: x*n


def make_divider(n): return lambda x: x/n


def indexclip(s, e, *a): return [b[int(s):int(e)] for b in a]


def angle_difference(a, b, degrees=False):
    if degrees: p = 180.0
    else: p = np.pi
    return np.mod(np.unwrap(a, p) - np.unwrap(b, p) + p, 2 * p) - p


def rad2deg360(x):
    """
    
    """
    d = np.rad2deg(x)
    d[d < 0] += 360
    return d
    

def rmnans(x, *a):
    """Remove values from array(s), using NaNs in key array.

    Examples
    --------
    >>> b = np.array([0,1,nan,3])
    >>> c = np.ones(b.shape)
    >>> bn, cn = rmnans(b,c)
    >>> bn
    array([ 0.,  1.,  3.])
    >>> cn
    array([ 1.,  1.,  1.])

    """
    mask = np.isnan(x)
    y = [x[~mask]]
    for b in a: y.append(b[~mask])
    return y


def plot_date_blocks(t, v, axes, colormap=None, unit_height=False, **kw):
    #TODO logic to check edges & heights for sanity
#    if kw.has_key('ec') or kw.has_key('edgecolor'): 
#        pass
#    else:
#        kw.update(dict(edgecolor='red'))
    d = np.diff(v)
    left = np.hstack((t[0],t[d.nonzero()]))
    right = np.hstack((t[d.nonzero()],mpl.dates.num2date(axes.get_xlim()[-1])))
    height = np.hstack((v[d.nonzero()], v[-1]))
    norm_height = height / np.float(np.max(height))
    for l, r, h, nh  in itertools.izip(left, right, height, norm_height):
        # draw a rectangle with the appropriate color
        if colormap:
            kw.update(dict(color = colormap(nh)))
        if unit_height: 
            h = 1 # do this _after_ colormap
        ll = (mpl.dates.date2num(l),0)
        w = mpl.dates.date2num(r) - mpl.dates.date2num(l)
        axes.add_patch(mpl.patches.Rectangle(ll, w, h, **kw))
    pt = np.vstack((left, right))
    pv = np.vstack((height, height))
    axes.plot_date(pt.ravel('F'), pv.ravel('F'), 'k-')

# TODO modify to use PatchCollection and set colors that way
# http://matplotlib.org/examples/api/patch_collection.html


def slant_range_and_depths_to_horizontal_range(r, d1, d2):
    """
    Compute the radius of a circle on a sphere (half-chord on a circle)
    using the Pythagorean theorem, the sphere radius, and the apothem (in
    this case, the difference in depths).

    Sphere radius must be greater than difference in depths.

    Examples
    --------
    >>> depth_corrected_range(10, 5, 9)
    # TODO
    """
    return (r**2 - (d1 - d2)**2) **0.5


def loadmtx(filename):
    """Read matrix from `.mtx` file

    The first two elements in a `.mtx` file are matrix dimensions encoded as 
    32-bit integers, and the rest of the file is a column major matrix of 
    single precision (i.e., 32-bit float).

    Note that the endianness may be different depending on platform, so 
    `.mtx` files may not be portable. This method is primarily intended to
    handle files sent to and from vehicles in the field over low-badwidth
    communication channels (e.g., Iridium SBD), and for development on
    techniques that use those files. Please use HDF5, NetCDF, MATLAB, or 
    numpy.save methods for any other use cases.

    Parameters
    ----------
    filename : str
        The file to load the matrix from.

    Returns
    -------
    a : array
        A numpy array containing the matrix saved in the file.

    Examples
    --------
    TODO

    See also: savemtx, numpy.fromfile, numpy.save, numpy.savez

    """
    with open(filename, 'rb') as f:
        shape = np.fromfile(file=f, dtype=np.int32, count=2) 
        # not sure why the .mtx file has its dimensions flipped, but this 
        # reads consistent with SF's fort_read & fort_readColumns
        return np.fromfile(file=f,dtype=np.float32).reshape(shape,order='F').T


def savemtx(a, filename):
    """Save array as a matrix in a `.mtx` file

    The first two elements in a `.mtx` file are matrix dimensions encoded as 
    32-bit integers, and the rest of the file is a column major matrix of 
    single precision (i.e., 32-bit float).

    Note that the endianness may be different depending on platform, so 
    `.mtx` files may not be portable. This method is primarily intended to
    handle files sent to and from vehicles in the field over low-badwidth
    communication channels (e.g., Iridium SBD), and for development on
    techniques that use those files. Please use HDF5, NetCDF, MATLAB, or 
    numpy.save methods for any other use cases.

    Parameters
    ----------
    a : array-like
        The array to be saved.
    filename : str
        The file to load the matrix from.

    Examples
    --------
    TODO

    See also: loadmtx, numpy.fromfile, numpy.save, numpy.savez

    """
    with open(filename, 'wb') as f:
        f.write(np.array(a.shape, dtype=np.int32).tostring(order='F'))
        f.write(a.astype(np.float32).tostring(order='F'))

