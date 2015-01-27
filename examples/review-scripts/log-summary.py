#!/usr/bin/env python
import matplotlib.pyplot as plt
import okeanidanalysis as oa

def main(logfile, verbose=0):
    """summarize an LRAUV log file with plots

    """
    if type(logfile) is not str: s = oa.logs.OkeanidLog(logfile.name)
    else: s = oa.logs.OkeanidLog(logfile)
    
    map_fig = plt.figure()
    mbm = oa.maps.MontereyBay(resolution='h')
    mbm.drawdefault()
    s.map_track(mbm, 'universal', 'k-', start_stop_marker=True)
    
    vplane_fig = plt.figure()
    s.vplane(fig=vplane_fig)

    plt.show()
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='plot summary of LRAUV log')
    logfile = parser.add_argument('logfile', type=argparse.FileType('rb'),
        help='the log to summarize in plots')
    parser.add_argument('-V', '--version', action='version', 
        version='%(prog)s 0.0.1',
        help='display version information and exit')
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='display verbose output')
    args = parser.parse_args()
    main(**args.__dict__)
