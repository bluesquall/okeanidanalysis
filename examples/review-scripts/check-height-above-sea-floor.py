#!/usr/bin/env python

import matplotlib.pyplot as plt

import okeanidanalysis as oa

def compare_heights_above_sea_floor(slates):
    fig = plt.figure()
    for s in slates:
        s.plot_timeseries('height_above_sea_floor', color='black', linewidth=2)
        s.plot_timeseries('NavChart/height_above_sea_floor', color='blue')
        try:
            s.plot_timeseries('DVL_micro/height_above_sea_floor', color='red')
        except:
            pass
        try:
            s.plot_timeseries('Rowe_600/height_above_sea_floor', color='red')
        except:
            pass
    plt.ylabel('height above sea floor [m]')
    plt.legend()
    return fig

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('logs', type=argparse.FileType('rb'), nargs='+',
            help='list of desired logs')
    args = parser.parse_args()
    slates = [oa.logs.OkeanidLog(log.name) for log in args.logs]
    fig = compare_heights_above_sea_floor(slates)
    plt.show()

