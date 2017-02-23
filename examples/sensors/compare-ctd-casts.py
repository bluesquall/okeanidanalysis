#!/usr/bin/env python
'''
This script compares the data collected by LRAUV _Tethys_ and the CTD rosette
deployed by R/V _Rachel Carson_ in the vicinity of M1 (36.747, -122.022) on
2015-06-04.

Tethys ran the actual mission after this command:

2015-06-04 16:46:57 tethys run, by: Brian Kieft, id: 3542139, Overload. Trying again, (sched asap "load Science/spiral_cast.xml;set spiral_cast.Depth01 100 meter;set spiral_cast.Depth02 30 meter;set spiral_cast.Depth03 30 meter;set spiral_cast.Depth04 20 meter;set spiral_cast.Depth05 20 meter;set spiral_cast.Depth06 10 meter" 4nym9 1 2
sched asap "set spiral_cast.Depth07 10 meter;set spiral_cast.Depth08 0.5 meter;set spiral_cast.Depth09 0.5 meter;set spiral_cast.MaxDepth 125 meter;run " 4nym9 2 2)

The timespan we are interested in is roughly:

[2015-06-04 16:40:00.000, 2015-06-04 18:00:00.000]
[2015-07-07 16:10:00.000, 2015-07-07 17:00:00.000]


'''

import os
import datetime
import numpy as np
import scipy
import scipy.io

import matplotlib
import matplotlib.dates
import matplotlib.pyplot as plt

import gsw

import okeanidanalysis as oa


dstart = datetime.datetime(2015,7,7,16,10,0)
dend = datetime.datetime(2015,7,7,17,0,0)
ddelta = datetime.timedelta(seconds=1)

r = scipy.io.loadmat(os.path.expanduser('~/Downloads/pctd_4_jordan_18815.mat'))['B'][0][0]
s = oa.logs.OkeanidLog('/mbari/LRAUV/tethys/missionlogs/2015/20150706_20150707/20150707T015732/201507070157_201507072348.mat')
t = matplotlib.dates.drange(dstart,dend,ddelta)
delta_C = 0.03 # We don't have an offset to directly compare the conductivity.
delta_T = -273.15 # Kelvin to Celsius, since engineering logs currently unserialize temperature in Kelvin
delta_P = 0 # We don't have an offset to directly compare the pressure.
delta_S = 0 #np.mean([34.5886 - 33.1413, 34.6348 - 32.9238]) # offset from comparison in test tank (currently a manual procedure)

print('Salinity offset: {0} [‰]'.format(delta_S))

rosette = dict( t=r['date_time']-366, # subtract 366 from MATLAB datenum to get matplotlib datenum
                latitude=r['dec_lat'],
                longitude=r['dec_long'],
                depth=r['rdep'],
                sea_water_electrical_conductivity=r['conduct'],
                sea_water_temperature=r['tmp'],
                sea_water_pressure=r['pressure'],
                sea_water_salinity=r['sal'],
              )
# TODO: Add density, chla, oxygen, ...
tethys = dict( t=t,
               latitude=s.interpolate_timeseries('latitude',t),
               longitude=s.interpolate_timeseries('longitude',t),
               depth=s.interpolate_timeseries('depth',t),
               sea_water_electrical_conductivity=s.interpolate_timeseries('sea_water_electrical_conductivity',t) + delta_C,
               sea_water_temperature=s.interpolate_timeseries('sea_water_temperature',t) + delta_T,
               sea_water_pressure=s.interpolate_timeseries('sea_water_pressure',t) + delta_P,
               sea_water_salinity=s.interpolate_timeseries('sea_water_salinity',t) + delta_S,
             )
"""
C, tNB = s.timeseries('sea_water_electrical_conductivity')
T, tNB = s.timeseries('sea_water_temperature')
P, tNB = s.timeseries('sea_water_pressure')
print(C.shape, T.shape, P.shape) # XXX Pressure can end up with different number of entries than C&T?
cSP = gsw.SP_from_C(C + delta_C, T + delta_T, P + delta_P)
cSPi = sp.interpolate.interp1d(tNB, cSP, bounds_error=False)
tethys.update(dict(calculated_sea_water_salinity=cSPi(t)))
"""
cSP = gsw.SP_from_C(tethys['sea_water_electrical_conductivity'] * 10, # XXX factor of 10 suspected to be a units thing...
                    tethys['sea_water_temperature'],
                    tethys['sea_water_pressure'])
tethys.update(dict(calculated_sea_water_salinity=cSP))

# TODO: Put the above data into a nc4 group instead of dictionaries.
# TODO: Resample the LRAUV data by depth-binning for a direct comparison to the rosette data.

fig, axs = plt.subplots(1, 4, sharey=True)
ax_conductivity, ax_temperature, ax_pressure, ax_salinity = axs

rkw = dict(label='rosette', linewidth=1, linestyle='dotted')
ax_conductivity.plot(rosette['sea_water_electrical_conductivity'], rosette['depth'], **rkw)
ax_temperature.plot(rosette['sea_water_temperature'], rosette['depth'],  **rkw)
ax_pressure.plot(rosette['sea_water_pressure'], rosette['depth'],  **rkw)
ax_salinity.plot(rosette['sea_water_salinity'], rosette['depth'],  **rkw)

tkw = dict(label='Tethys', linewidth=2, linestyle='solid')
ax_conductivity.plot(tethys['sea_water_electrical_conductivity'], tethys['depth'], **tkw)
ax_temperature.plot(tethys['sea_water_temperature'], tethys['depth'], **tkw)
ax_pressure.plot(tethys['sea_water_pressure'], tethys['depth'], **tkw)
ax_salinity.plot(tethys['sea_water_salinity'], tethys['depth'], **tkw)
ax_salinity.plot(tethys['calculated_sea_water_salinity'], tethys['depth'], color='m', **tkw)

ax_conductivity.set_ylim([500,0])
ax_conductivity.set_xlim([3.3,3.9])
ax_temperature.set_xlim([6,13])
ax_pressure.set_xlim([0,500])
ax_salinity.set_xlim([31,35])

ax_conductivity.set_ylabel('depth [m]')
ax_conductivity.set_xlabel('conductivity [_]') # CTD interface lists units as mmho/cm, but unserialized data just has an underscore
ax_temperature.set_xlabel('temperature [degC]')
ax_pressure.set_xlabel('pressure [db]')
ax_salinity.set_xlabel('salinity [‰]')

# automatic locator & formatter for salinity makes something you can't really read -- fix it
ax_salinity.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
ax_salinity.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))

vehicle = s.filename.split('/')[3]
logset = s.filename.split('/')[-2]
plt.suptitle('{0} {1}'.format(vehicle, logset))

plt.show()
