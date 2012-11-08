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
    dlon, dlat, dv = oa.lib.gridravel(oma.longitude, oma.latitude, oma.v)
    dtos.append(dto)
    utimes.append(utime)
    dus.append(du)
    dvs.append(dv)
du = np.array(dus)
dv = np.array(dvs)
utime = np.array(utimes)

u_eof.insert_maps(dlon, dlat, du, utime)
v_eof.insert_maps(dlon, dlat, dv, utime)

u_eof.calculate(detrend=False)
v_eof.calculate(detrend=False)

cfkw = dict(levels=np.arange(-1,1.1,0.1), latlon=True)
n = 2**5 # number of modes to use in reconstruction

u = u_eof.extract_maps(n=n)
v = v_eof.extract_maps(n=n)

fig = plt.figure()
for k, t in enumerate(utime):
    dto = datetime.datetime.utcfromtimestamp(np.floor(t / 1e6))
    plt.clf() #TODO probably a faster way than starting over...
    m = oa.maps.MontereyBay(resolution='h')
    m.drawdefault(), m.drawcoastlines(), m.drawgrid()
    m.draw_currents(glat, glon, u[k], v[k])
    plt.title('{0}, {1} modes'.format(dto, n))
    plt.savefig('/tmp/oma-currents-eofs-{0}modes-{1:06d}.png'.format(n,k))

print "cd to /tmp & run:"
print "ffmpeg -f image2 -qscale 1 -r 10 -i ./oma-currents-eofs-{0}modes-%06d.png oma-currents-eofs-time.mp4".format(n)
