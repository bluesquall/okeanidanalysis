#!/usr/bin/env python
"""
Empirical Orthogonal Functions on OMA surface currents
======================================================

Open Boundary Modal Analysis 

"""
import datetime
import numpy as np
import matplotlib.pyplot as plt
import oceanidanalysis as oa

# evaluate EOFs separately for now
u_eof = oa.eof.EOF()
v_eof = oa.eof.EOF()

# get some example data
oma = oa.currents.OpenBoundaryModalAnalysis()
dtostart = datetime.datetime(2012,01,01,0,0)
oma.open_datetime_url(dtostart)
glon, glat = np.meshgrid(oma.longitude, oma.latitude)

dtos, utimes, dus, dvs = [], [], [], []
for h in range(2**7):
    tdelta = datetime.timedelta(hours = h)
    dto = dtostart + tdelta
    utime = oa.lib.utime(dto)
    oma.open_datetime_url(dto)
    dlon, dlat, du = oa.lib.gridravel(oma.longitude, oma.latitude, oma.u)   
    #TODO confirm dlon, dlat unchanged...
#    dlon, dlat, dv = oa.lib.gridravel(oma.longitude, oma.latitude, oma.v)
    dtos.append(dto)
    utimes.append(utime)
    dus.append(du)
#    dvs.append(dv)
du = np.array(dus)
dv = np.array(dvs)
utime = np.array(utimes)


u_eof.insert_maps(dlon, dlat, du, utime)
# v_eof.insert_maps(dlon, dlat, dv, utime)

u_eof.calculate(detrend=False)
# v_eof.calculate()

e = u_eof.extract_maps()
c = u_eof.EC

# re-open a specific oma set
tdelta = datetime.timedelta(hours = 6)
dto = dtostart + tdelta
oma.open_datetime_url(dto)

cfkw = dict(levels=np.arange(-1,1.1,0.1), latlon=True)
k = np.where(utime == oa.lib.utime(dto))[0][0]
print k
n = 2**6 # number of modes to use in reconstruction

for p in range(2**7):
    fig = plt.figure(p)
    m = oa.maps.MontereyBay(resolution='i')
    m.drawdefault(), m.drawcoastlines(), m.drawgrid()
    m.contourf(glon, glat, oma.u - u_eof.extract_maps(n=p)[k], latlon=True,
            levels=np.arange(-01,1.1,0.1)/10)
    plt.colorbar()
    plt.title('original data - first {} modes'.format(p))
    plt.savefig('/tmp/oma-currents-eofs-u-{0:06d}.png'.format(p))

print "cd to /tmp & run:"
print "ffmpeg -f image2 -i ./oma-currents-eofs-u-%06d.png oma-currents-eofs-u.mpg"
