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

oma = oa.currents.OpenBoundaryModalAnalysis()

dtos, utimes, dus, dvs = [], [], [], []
for hour in range(23):
    dto = datetime.datetime(2012,10,01,hour,0)
    utime = oa.lib.utime(dto)
    oma.open_datetime_url(dto)
    dlon, dlat, du = oa.lib.gridravel(oma.longitude, oma.latitude, oma.u)   
#    dlon, dlat, dv = oa.lib.gridravel(oma.longitude, oma.latitude, oma.v)
    dtos.append(dto)
    utimes.append(utime)
    dus.append(du)
#    dvs.append(dv)
du = np.array(dus)

print dlon.shape, dlat.shape, du.shape

u_eof.insert_maps(dlon, dlat, du, utimes)
# v_eof.insert_maps(dlon, dlat, np.array(dv), utimes)

u_eof.calculate()
# v_eof.calculate()

#print u_eof.xd.shape
#print u_eof.yd.shape
#print u_eof.zd.shape
#print u_eof.td.shape


e = u_eof.extract_maps()
c = u_eof.EC

print u_eof.EC.shape

glon, glat = np.meshgrid(oma.longitude, oma.latitude)

fig = plt.figure(0)
m = oa.maps.MontereyBay(resolution='i')
m.drawdefault() 
m.contourf(glon, glat, e[0], 50, latlon=True)
m.drawgrid()
plt.title('EOF mode 0')

fig = plt.figure(1)
m = oa.maps.MontereyBay(resolution='i')
m.drawdefault() 
m.contourf(glon, glat, e[1], 50, latlon=True)
m.drawgrid()
plt.title('EOF mode 1')


fig = plt.figure(10)
ax = fig.add_subplot(1,1,1)
# ax.plot_date(dtos, c[0])
ax.plot(u_eof.EC)

fig = plt.figure(20)
m = oa.maps.MontereyBay(resolution='i')
m.drawdefault() 
m.contourf(glon, glat, oma.u, 50, latlon=True)
m.drawgrid()
plt.title('original data')

fig = plt.figure(21)
m = oa.maps.MontereyBay(resolution='i')
m.drawdefault() 
m.contourf(glon, glat, u_eof.extract_maps(n=20)[-1], 50, latlon=True)
m.drawgrid()
plt.title('first 20 modes')



plt.show()
