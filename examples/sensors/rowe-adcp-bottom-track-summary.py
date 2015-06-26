#!/bin/env python
"""
e.g.: $ python rowe-adcp-bottom-track-summary.py /mbari/LRAUV/makai/missionlogs/devel/20150617-ADCP-in-tank/20150617T172914/ADCP-2015061717.ENS.mat
"""

import numpy as np
import scipy as sp
import scipy.io
import matplotlib.pyplot as plt


def plot_adcp_bottom_track_summary(infile, save=True, show=True, autoscale_ylims=False):
    
    if infile.endswith('ENS.mat'):
        bt = sp.io.loadmat(infile)['E000010'].squeeze()
        idx = 14 # TODO: There may be some sort of misalignment in ENS files...
        vr = bt[:,idx:idx+4].squeeze()
        snr = bt[:,idx+4:idx+8].squeeze()
        amp = bt[:,idx+8:idx+12].squeeze()
        cor = bt[:,idx+12:idx+16].squeeze()
        bv = bt[:,idx+16:idx+20].squeeze()
        bnum = bt[:,idx+20:idx+24].squeeze()
        iv = bt[:,idx+24:idx+28].squeeze()
        inum = bt[:,idx+28:idx+32].squeeze()
    elif infile.endswith('mat'):
        import okeanidanalysis
        s = okeanidanalysis.logs.OkeanidLog(infile)
        vr, t_vr = s.timeseries('Rowe_600.vertical_range')
        snr, t_snr = s.timeseries('Rowe_600.signal_to_noise')
        amp, t_amp = s.timeseries('Rowe_600.bottom_track_amplitude')
        cor, t_cor = s.timeseries('Rowe_600.bottom_track_correlation')
        bv, t_bv = s.timeseries('Rowe_600.bottom_track_beam_velocity')
        iv, t_iv = s.timeseries('Rowe_600.bottom_track_instrument_velocity')
    
    fig, axs = plt.subplots(6, 4, sharex=True, sharey='row', figsize=(6.5,9))
    vrax = axs[0]
    snrax = axs[1]
    ampax = axs[2]
    corax = axs[3]
    bvax = axs[4]
    ivax = axs[5]
    
    for i in range(4):
        vrax[i].plot(vr[:,i])
        snrax[i].plot(snr[:,i])
        ampax[i].plot(amp[:,i])
        corax[i].plot(cor[:,i])
        bvax[i].plot(bv[:,i])
        ivax[i].plot(iv[:,i])
    
    ylkw = dict(rotation='horizontal', horizontalalignment='right')
    vrax[0].set_ylabel('vertical\nrange [m]', **ylkw)
    snrax[0].set_ylabel('SNR [dB]', **ylkw)
    ampax[0].set_ylabel('amplitude [dB]', **ylkw)
    corax[0].set_ylabel('correlation [-]', **ylkw)
    bvax[0].set_ylabel('beam\nvelocity [m/s]', **ylkw)
    ivax[0].set_ylabel('instrument\nvelocity [m/s]', **ylkw)
    
    ivax[0].set_xlabel('ensemble number')
    
    for i, ax in enumerate(vrax): ax.set_title('beam {0}'.format(i))
    
    if not autoscale_ylims:
        vrax[0].set_ylim([0,125])
        snrax[0].set_ylim([0,100])
        ampax[0].set_ylim([0,200])
        corax[0].set_ylim([0,1])
        bvax[0].set_ylim([-2,2])
        ivax[0].set_ylim([-2,2])
    
    # TODO: Get the lines below to work.
    #print([t.get_text() for t in ivax[0].xaxis.get_majorticklabels()])
    #ivax[0].xaxis.set_ticklabels([t.get_text() for t in ivax[0].xaxis.get_majorticklabels()], rotation='vertical') # should propogate to ther x axes
    for ax in ivax:
       plt.sca(ax)
       plt.setp(plt.xticks()[1], rotation=90, fontsize=6)   
    fig.suptitle(infile.rsplit('/')[-1])
    
    plt.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.1, wspace=0)
    
    if save: fig.savefig('/tmp/{0}.png'.format(infile.rsplit('/')[-1]))
    
    if show: plt.show()
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='plot summary of ADCP bottom track data')
    parser.add_argument('-V', '--version', action='version',
        version='%(prog)s 0.0.1',
        help='display version information and exit')
    parser.add_argument('infile', metavar='filename',
        type=str, help='LRAUV slate or RTI .ENS unpacked into .mat')
    parser.add_argument('-y', '--autoscale-ylims', action='store_true')

    args = parser.parse_args()
    plot_adcp_bottom_track_summary(**args.__dict__)
