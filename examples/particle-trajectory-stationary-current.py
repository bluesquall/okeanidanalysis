#!/usr/bin/env python
"""
Particle trajectory in stationary surface currents
==================================================

"""
import datetime
import numpy as np
import scipy as sp
import scipy.interpolate
import matplotlib.pyplot as plt
import pyproj
import oceanidanalysis as oa



# get some example data
oma = oa.currents.OpenBoundaryModalAnalysis()
dtostart = datetime.datetime(2012,12,01,0,0)
oma.open_datetime_url(dtostart)
glon, glat = np.meshgrid(oma.longitude, oma.latitude)

# for now, interpolate currents directly in lat/lon
#iu = sp.interpolate.RectBivariateSpline(oma.longitude, oma.latitude, oma.u)
#iv = sp.interpolate.RectBivariateSpline(oma.longitude, oma.latitude, oma.v)

# for now, perform meters calculations in UTM
# TODO in the future, use locally-centered NED frame at each instant
latlon = pyproj.Proj(proj='latlong', datum='WGS84')
utm = pyproj.Proj(proj='utm', zone=10, datum='WGS84') # MB in S10
# define initial position in lat/lon; convert to UTM (meters)
lat0 = 36.75
lon0 = -122
# x0, y0 = pyproj.transform(latlon, utm, lon0, lat0)




fig = plt.figure(0)
m = oa.maps.MontereyBay(resolution='h')
m.drawdefault(), m.drawcoastlines(), m.drawgrid()
m.draw_currents(oma.latitude, oma.longitude, oma.u, oma.v)
#TODO consider adjusting draw_currents to accept just a surfaceCurrent object
#print trajectory
lat0s = np.arange(36.5, 37, 0.05)
lon0s = np.arange(-122.5, -121.8, 0.05)
# print lat0s
# print lon0s
particles = [oa.currents.Particle(lat0, lon0) 
        for lat0 in lat0s for lon0 in lon0s]
for p in particles:
    trajectory = p.advect(oma.interpolate, np.arange(0.25*60*60,0,-60))
    x, y = m(trajectory[:,1], trajectory[:,0])
    m.scatter(x,y,3,marker='o',color='r')

plt.show()
