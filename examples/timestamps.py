#!/usr/bin/env python

import time, datetime, pytz
import numpy as np
import matplotlib as mpl
import matplotlib.dates

import okeanidanalysis as oa

def main(logfile):

    if type(logfile) is not str: s = oa.logs.OkeanidLog(logfile.name)
    else: s = oa.logs.OkeanidLog(logfile)

    # LRAUV logs saved as `.mat` files in HDF5 format use the MATLAB datenum. The timezone is UTC, but that is not explicitly stated in the log file.
    start_matlab_datenum = s['depth/time'][0][0]

    # If you access a timeseries using the OkeanidLog.timeseries method, you will get a matplotlib datenum
    depth, t_depth = s.timeseries('depth')
    start_matplotlib_datenum = t_depth[0]

    print('matplotlib datenum is {0} less than MATLAB datenum (should be 366)'.format(start_matlab_datenum-start_matplotlib_datenum))

    # You can use methods in matplotlib.dates to convert easily to python datetime objects
    python_datetime_depth = matplotlib.dates.num2date(t_depth, tz=pytz.UTC)
    start_python_datetime = python_datetime_depth[0]

    # or to epoch seconds
    unix_epoch_depth = matplotlib.dates.num2epoch(t_depth)
    start_unix_epoch = unix_epoch_depth[0]

    # or to epoch milliseconds (i.e., mtime)
    mtime_depth = np.rint(matplotlib.dates.num2epoch(t_depth) * 1e3).astype(np.uint64)
    start_mtime = mtime_depth[0]

    # or to epoch microseconds (i.e., utime)
    utime_depth = np.rint(matplotlib.dates.num2epoch(t_depth) * 1e6).astype(np.uint64)
    start_utime = utime_depth[0]

    msg = 'Depth record starts at:\n\t{0}\n\t{1} [Unix epoch seconds]\n\t{2} [Unix epoch milliseconds]\n\t{3} [Unix epoch microseconds]\n\t{4} [matplotlib days]\n\t{5} [matlab days]'
    print(msg.format(start_python_datetime, start_unix_epoch, start_mtime, start_utime, start_matplotlib_datenum, start_matlab_datenum))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='explain timestamps in LRAUV log')
    logfile = parser.add_argument('logfile', type=argparse.FileType('rb'),
        help='the log to use in the example')
    parser.add_argument('-V', '--version', action='version',
        version='%(prog)s 0.0.1',
        help='display version information and exit')
    args = parser.parse_args()
    main(**args.__dict__)
